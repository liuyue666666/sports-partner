from fastapi import APIRouter, Query

from app.config import settings
from app.dependencies import CurrentUser, DbSession, OptionalUserId
from app.schemas.activity import ActivityCreateIn, ActivityDetailOut, ActivityOut
from app.services.activity_service import activity_service

router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("", response_model=ActivityDetailOut)
def create_activity(
    body: ActivityCreateIn,
    current_user: CurrentUser,
    db: DbSession,
) -> ActivityDetailOut:
    return activity_service.create(db, current_user, body)


@router.get("", response_model=list[ActivityOut])
def list_activities(
    db: DbSession,
    viewer_id: OptionalUserId = None,
    lat: float | None = Query(default=None, ge=-90, le=90),
    lng: float | None = Query(default=None, ge=-180, le=180),
    radius: int | None = Query(default=None, ge=100, le=50000),
    sport_tag_id: int | None = Query(default=None),
) -> list[ActivityOut]:
    return activity_service.list_activities(
        db,
        viewer_id=viewer_id,
        lat=lat,
        lng=lng,
        radius_meters=radius or settings.match_default_radius_meters,
        sport_tag_id=sport_tag_id,
    )


@router.get("/my/created", response_model=list[ActivityOut])
def list_my_created(current_user: CurrentUser, db: DbSession) -> list[ActivityOut]:
    return activity_service.list_my_created(db, current_user.id)


@router.get("/my/joined", response_model=list[ActivityOut])
def list_my_joined(current_user: CurrentUser, db: DbSession) -> list[ActivityOut]:
    return activity_service.list_my_joined(db, current_user.id)


@router.get("/{activity_id}", response_model=ActivityDetailOut)
def get_activity(
    activity_id: int,
    db: DbSession,
    viewer_id: OptionalUserId = None,
    lat: float | None = Query(default=None),
    lng: float | None = Query(default=None),
) -> ActivityDetailOut:
    return activity_service.get_detail(db, activity_id, viewer_id=viewer_id, lat=lat, lng=lng)


@router.post("/{activity_id}/join", response_model=ActivityDetailOut)
def join_activity(
    activity_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> ActivityDetailOut:
    return activity_service.join(db, activity_id, current_user)


@router.delete("/{activity_id}/join", response_model=ActivityDetailOut)
def cancel_join(
    activity_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> ActivityDetailOut:
    return activity_service.cancel_join(db, activity_id, current_user)


@router.put("/{activity_id}/cancel", response_model=ActivityDetailOut)
def cancel_activity(
    activity_id: int,
    current_user: CurrentUser,
    db: DbSession,
) -> ActivityDetailOut:
    return activity_service.cancel_activity(db, activity_id, current_user)
