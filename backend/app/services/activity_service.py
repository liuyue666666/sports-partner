from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.config import settings
from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.core.redis_client import get_redis
from app.models.activity import Activity, ActivityStatus, GenderRequirement, ParticipantStatus
from app.models.user import Gender, SportTag, User
from app.repositories.activity_repo import activity_repo
from app.repositories.user_repo import user_repo
from app.schemas.activity import ActivityCreateIn, ActivityDetailOut, ActivityOut, ParticipantOut
from app.schemas.user import UserPublicOut
from app.services.activity_location_service import (
    acquire_activity_lock,
    release_activity_lock,
    remove_activity_geo,
    set_activity_geo,
)
from app.utils.geo import haversine_distance_meters


def _ensure_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def _now() -> datetime:
    return datetime.now(timezone.utc)


class ActivityService:
    def refresh_activity_status(self, db: Session, activity: Activity) -> Activity:
        now = _now()
        start = _ensure_aware(activity.start_time)
        end = _ensure_aware(activity.end_time) if activity.end_time else start + timedelta(hours=2)

        if activity.status == ActivityStatus.CANCELLED.value:
            return activity

        if now >= end:
            activity.status = ActivityStatus.ENDED.value
        elif now >= start:
            activity.status = ActivityStatus.IN_PROGRESS.value
        elif activity.current_participants >= activity.max_participants:
            activity.status = ActivityStatus.FULL.value
        elif (
            activity.status == ActivityStatus.FULL.value
            and activity.current_participants < activity.max_participants
        ):
            activity.status = ActivityStatus.RECRUITING.value

        db.commit()
        db.refresh(activity)

        try:
            redis_client = get_redis()
            if activity.status == ActivityStatus.RECRUITING.value:
                set_activity_geo(
                    redis_client,
                    activity.id,
                    float(activity.longitude),
                    float(activity.latitude),
                )
            else:
                remove_activity_geo(redis_client, activity.id)
        except Exception:
            pass

        return activity

    def refresh_all_statuses(self, db: Session) -> None:
        for activity in activity_repo.list_for_status_refresh(db):
            self.refresh_activity_status(db, activity)

    def _is_joined(self, db: Session, activity_id: int, user_id: int | None) -> bool:
        if user_id is None:
            return False
        participant = activity_repo.get_participant(db, activity_id, user_id)
        return participant is not None and participant.status == ParticipantStatus.JOINED.value

    def _to_activity_out(
        self,
        db: Session,
        activity: Activity,
        *,
        viewer_id: int | None = None,
        lat: float | None = None,
        lng: float | None = None,
    ) -> ActivityOut:
        distance = None
        if lat is not None and lng is not None:
            distance = haversine_distance_meters(
                lat, lng, float(activity.latitude), float(activity.longitude)
            )
        return ActivityOut(
            id=activity.id,
            title=activity.title,
            description=activity.description,
            sport_tag=activity.sport_tag,
            start_time=activity.start_time,
            end_time=activity.end_time,
            latitude=float(activity.latitude),
            longitude=float(activity.longitude),
            address=activity.address,
            max_participants=activity.max_participants,
            current_participants=activity.current_participants,
            gender_requirement=activity.gender_requirement,
            registration_deadline=activity.registration_deadline,
            status=activity.status,
            cover_url=activity.cover_url,
            creator=UserPublicOut.model_validate(activity.creator),
            distance_meters=distance,
            is_joined=self._is_joined(db, activity.id, viewer_id),
            created_at=activity.created_at,
        )

    def _to_detail_out(
        self,
        db: Session,
        activity: Activity,
        *,
        viewer_id: int | None = None,
        lat: float | None = None,
        lng: float | None = None,
    ) -> ActivityDetailOut:
        base = self._to_activity_out(db, activity, viewer_id=viewer_id, lat=lat, lng=lng)
        participants = [
            ParticipantOut(
                user=UserPublicOut.model_validate(p.user),
                joined_at=p.joined_at,
            )
            for p in activity.participants
            if p.status == ParticipantStatus.JOINED.value
        ]
        return ActivityDetailOut(**base.model_dump(), participants=participants)

    def create(self, db: Session, creator: User, data: ActivityCreateIn) -> ActivityDetailOut:
        tag = db.get(SportTag, data.sport_tag_id)
        if not tag:
            raise NotFoundError("Sport tag not found")

        now = _now()
        if _ensure_aware(data.start_time) <= now:
            raise ConflictError("start_time must be in the future")
        if _ensure_aware(data.registration_deadline) <= now:
            raise ConflictError("registration_deadline must be in the future")

        activity = activity_repo.create(
            db,
            creator_id=creator.id,
            title=data.title,
            description=data.description,
            sport_tag_id=data.sport_tag_id,
            start_time=data.start_time,
            end_time=data.end_time,
            latitude=data.latitude,
            longitude=data.longitude,
            address=data.address,
            max_participants=data.max_participants,
            gender_requirement=int(data.gender_requirement),
            registration_deadline=data.registration_deadline,
            cover_url=data.cover_url,
            status=ActivityStatus.RECRUITING.value,
            current_participants=1,
        )

        try:
            redis_client = get_redis()
            set_activity_geo(redis_client, activity.id, data.longitude, data.latitude)
        except Exception:
            pass

        return self._to_detail_out(db, activity, viewer_id=creator.id)

    def list_activities(
        self,
        db: Session,
        *,
        viewer_id: int | None = None,
        lat: float | None = None,
        lng: float | None = None,
        radius_meters: int | None = None,
        sport_tag_id: int | None = None,
    ) -> list[ActivityOut]:
        self.refresh_all_statuses(db)
        activities = activity_repo.list_active(db, sport_tag_id=sport_tag_id)
        radius = radius_meters or settings.match_default_radius_meters

        results: list[ActivityOut] = []
        for activity in activities:
            item = self._to_activity_out(db, activity, viewer_id=viewer_id, lat=lat, lng=lng)
            if lat is not None and lng is not None and item.distance_meters is not None:
                if item.distance_meters > radius:
                    continue
            results.append(item)

        if lat is not None and lng is not None:
            results.sort(key=lambda x: x.distance_meters or float("inf"))
        return results

    def get_detail(
        self,
        db: Session,
        activity_id: int,
        *,
        viewer_id: int | None = None,
        lat: float | None = None,
        lng: float | None = None,
    ) -> ActivityDetailOut:
        activity = activity_repo.get_by_id(db, activity_id)
        if not activity:
            raise NotFoundError("Activity not found")
        self.refresh_activity_status(db, activity)
        activity = activity_repo.get_by_id(db, activity_id)
        assert activity
        return self._to_detail_out(db, activity, viewer_id=viewer_id, lat=lat, lng=lng)

    def list_my_created(self, db: Session, user_id: int) -> list[ActivityOut]:
        activities = activity_repo.list_by_creator(db, user_id)
        return [self._to_activity_out(db, a, viewer_id=user_id) for a in activities]

    def list_my_joined(self, db: Session, user_id: int) -> list[ActivityOut]:
        activities = activity_repo.list_joined_by_user(db, user_id)
        return [self._to_activity_out(db, a, viewer_id=user_id) for a in activities]

    def _check_gender(self, activity: Activity, user: User) -> None:
        req = activity.gender_requirement
        if req == GenderRequirement.MALE_ONLY.value and user.gender != Gender.MALE.value:
            raise ForbiddenError("This activity is for males only")
        if req == GenderRequirement.FEMALE_ONLY.value and user.gender != Gender.FEMALE.value:
            raise ForbiddenError("This activity is for females only")

    def join(self, db: Session, activity_id: int, user: User) -> ActivityDetailOut:
        activity = activity_repo.get_by_id(db, activity_id)
        if not activity:
            raise NotFoundError("Activity not found")

        self.refresh_activity_status(db, activity)
        db.refresh(activity)

        if activity.status not in (ActivityStatus.RECRUITING.value, ActivityStatus.FULL.value):
            raise ConflictError("Activity is not open for registration")
        if activity.creator_id == user.id:
            raise ConflictError("Creator is already in the activity")
        if _now() > _ensure_aware(activity.registration_deadline):
            raise ConflictError("Registration deadline has passed")

        self._check_gender(activity, user)

        existing = activity_repo.get_participant(db, activity_id, user.id)
        if existing and existing.status == ParticipantStatus.JOINED.value:
            raise ConflictError("Already joined")

        redis_client = None
        locked = False
        try:
            redis_client = get_redis()
            locked = acquire_activity_lock(redis_client, activity_id)
            if not locked:
                raise ConflictError("Activity is busy, please retry")
        except ConflictError:
            raise
        except Exception:
            locked = False

        try:
            db.refresh(activity)
            if activity.current_participants >= activity.max_participants:
                raise ConflictError("Activity is full")

            if existing:
                existing.status = ParticipantStatus.JOINED.value
                existing.joined_at = _now()
            else:
                activity_repo.add_participant(db, activity_id, user.id)

            activity.current_participants += 1
            if activity.current_participants >= activity.max_participants:
                activity.status = ActivityStatus.FULL.value

            activity_repo.create_message(
                db,
                activity.creator_id,
                "有人加入活动",
                f"{user.nickname} 加入了「{activity.title}」",
            )
            db.commit()
        finally:
            if locked and redis_client:
                release_activity_lock(redis_client, activity_id)

        activity = activity_repo.get_by_id(db, activity_id)
        assert activity
        return self._to_detail_out(db, activity, viewer_id=user.id)

    def cancel_join(self, db: Session, activity_id: int, user: User) -> ActivityDetailOut:
        activity = activity_repo.get_by_id(db, activity_id)
        if not activity:
            raise NotFoundError("Activity not found")
        if activity.creator_id == user.id:
            raise ConflictError("Creator cannot cancel join; cancel the activity instead")

        participant = activity_repo.get_participant(db, activity_id, user.id)
        if not participant or participant.status != ParticipantStatus.JOINED.value:
            raise ConflictError("Not joined")

        if activity.status == ActivityStatus.IN_PROGRESS.value:
            raise ConflictError("Cannot cancel during activity")

        participant.status = ParticipantStatus.CANCELLED.value
        activity.current_participants = max(1, activity.current_participants - 1)
        if activity.status == ActivityStatus.FULL.value:
            activity.status = ActivityStatus.RECRUITING.value

        db.commit()
        activity = activity_repo.get_by_id(db, activity_id)
        assert activity
        return self._to_detail_out(db, activity, viewer_id=user.id)

    def cancel_activity(self, db: Session, activity_id: int, user: User) -> ActivityDetailOut:
        activity = activity_repo.get_by_id(db, activity_id)
        if not activity:
            raise NotFoundError("Activity not found")
        if activity.creator_id != user.id:
            raise ForbiddenError("Only creator can cancel the activity")
        if activity.status in (ActivityStatus.ENDED.value, ActivityStatus.CANCELLED.value):
            raise ConflictError("Activity already ended or cancelled")

        activity.status = ActivityStatus.CANCELLED.value
        for p in activity.participants:
            if p.status == ParticipantStatus.JOINED.value and p.user_id != user.id:
                activity_repo.create_message(
                    db,
                    p.user_id,
                    "活动已取消",
                    f"「{activity.title}」已被发起人取消",
                )
        db.commit()

        try:
            remove_activity_geo(get_redis(), activity_id)
        except Exception:
            pass

        activity = activity_repo.get_by_id(db, activity_id)
        assert activity
        return self._to_detail_out(db, activity, viewer_id=user.id)


activity_service = ActivityService()
