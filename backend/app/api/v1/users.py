from fastapi import APIRouter

from app.dependencies import CurrentUser, DbSession
from app.repositories.user_repo import user_repo
from app.schemas.user import LocationUpdateIn, SportTagOut, UserOut, UserPublicOut, UserUpdateIn
from app.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def get_me(current_user: CurrentUser, db: DbSession) -> UserOut:
    return user_service.get_me(db, current_user.id)


@router.put("/me", response_model=UserOut)
def update_me(body: UserUpdateIn, current_user: CurrentUser, db: DbSession) -> UserOut:
    return user_service.update_me(db, current_user.id, body)


@router.post("/location", response_model=UserOut)
def update_location(
    body: LocationUpdateIn,
    current_user: CurrentUser,
    db: DbSession,
) -> UserOut:
    return user_service.update_location(db, current_user.id, body)


@router.get("/{user_id}", response_model=UserPublicOut)
def get_user(user_id: int, db: DbSession) -> UserPublicOut:
    return user_service.get_public_profile(db, user_id)


sport_tags_router = APIRouter(prefix="/sport-tags", tags=["sport-tags"])


@sport_tags_router.get("", response_model=list[SportTagOut])
def list_sport_tags(db: DbSession) -> list[SportTagOut]:
    tags = user_repo.list_sport_tags(db)
    return [SportTagOut.model_validate(tag) for tag in tags]
