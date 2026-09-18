from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session, selectinload

from app.models.activity import (
    Activity,
    ActivityParticipant,
    ActivityStatus,
    ParticipantStatus,
)
from app.models.user import Message, SportTag, User


class ActivityRepository:
    def get_by_id(self, db: Session, activity_id: int) -> Activity | None:
        return (
            db.query(Activity)
            .options(
                selectinload(Activity.creator).selectinload(User.sport_tags),
                selectinload(Activity.sport_tag),
                selectinload(Activity.participants)
                .selectinload(ActivityParticipant.user)
                .selectinload(User.sport_tags),
            )
            .filter(Activity.id == activity_id)
            .first()
        )

    def list_active(
        self,
        db: Session,
        *,
        sport_tag_id: int | None = None,
        status: int | None = None,
    ) -> list[Activity]:
        query = (
            db.query(Activity)
            .options(selectinload(Activity.creator), selectinload(Activity.sport_tag))
            .filter(
                Activity.status.in_([
                    ActivityStatus.RECRUITING.value,
                    ActivityStatus.FULL.value,
                    ActivityStatus.IN_PROGRESS.value,
                ])
            )
        )
        if sport_tag_id is not None:
            query = query.filter(Activity.sport_tag_id == sport_tag_id)
        if status is not None:
            query = query.filter(Activity.status == status)
        return query.order_by(Activity.start_time.asc()).all()

    def list_by_creator(self, db: Session, creator_id: int) -> list[Activity]:
        return (
            db.query(Activity)
            .options(selectinload(Activity.creator), selectinload(Activity.sport_tag))
            .filter(Activity.creator_id == creator_id)
            .order_by(Activity.created_at.desc())
            .all()
        )

    def list_joined_by_user(self, db: Session, user_id: int) -> list[Activity]:
        return (
            db.query(Activity)
            .join(ActivityParticipant)
            .options(selectinload(Activity.creator), selectinload(Activity.sport_tag))
            .filter(
                ActivityParticipant.user_id == user_id,
                ActivityParticipant.status == ParticipantStatus.JOINED.value,
            )
            .order_by(Activity.start_time.asc())
            .all()
        )

    def get_participant(
        self, db: Session, activity_id: int, user_id: int
    ) -> ActivityParticipant | None:
        return (
            db.query(ActivityParticipant)
            .filter(
                ActivityParticipant.activity_id == activity_id,
                ActivityParticipant.user_id == user_id,
            )
            .first()
        )

    def create(self, db: Session, *, creator_id: int, **fields) -> Activity:
        activity = Activity(creator_id=creator_id, **fields)
        db.add(activity)
        db.flush()
        db.add(
            ActivityParticipant(
                activity_id=activity.id,
                user_id=creator_id,
                status=ParticipantStatus.JOINED.value,
            )
        )
        db.commit()
        db.refresh(activity)
        return self.get_by_id(db, activity.id) or activity

    def add_participant(self, db: Session, activity_id: int, user_id: int) -> ActivityParticipant:
        participant = ActivityParticipant(
            activity_id=activity_id,
            user_id=user_id,
            status=ParticipantStatus.JOINED.value,
        )
        db.add(participant)
        return participant

    def create_message(self, db: Session, user_id: int, title: str, content: str) -> None:
        db.add(Message(user_id=user_id, title=title, content=content))

    def list_for_status_refresh(self, db: Session) -> list[Activity]:
        now = datetime.now(timezone.utc)
        return (
            db.query(Activity)
            .filter(
                Activity.status.in_([
                    ActivityStatus.RECRUITING.value,
                    ActivityStatus.FULL.value,
                    ActivityStatus.IN_PROGRESS.value,
                ]),
                Activity.start_time <= now + timedelta(days=1),
            )
            .all()
        )


activity_repo = ActivityRepository()
