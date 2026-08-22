from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.core.redis_client import get_redis
from app.repositories.user_repo import user_repo
from app.schemas.user import LocationUpdateIn, UserOut, UserPublicOut, UserUpdateIn
from app.services.location_service import set_user_geo, set_user_online


def _to_user_out(user) -> UserOut:
    return UserOut.model_validate(user)


def _to_public_out(user) -> UserPublicOut:
    return UserPublicOut.model_validate(user)


class UserService:
    def get_me(self, db: Session, user_id: int) -> UserOut:
        user = user_repo.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User not found")
        return _to_user_out(user)

    def get_public_profile(self, db: Session, user_id: int) -> UserPublicOut:
        user = user_repo.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User not found")
        return _to_public_out(user)

    def update_me(self, db: Session, user_id: int, data: UserUpdateIn) -> UserOut:
        user = user_repo.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User not found")
        updated = user_repo.update_profile(db, user, data)
        return _to_user_out(updated)

    def update_location(self, db: Session, user_id: int, data: LocationUpdateIn) -> UserOut:
        user = user_repo.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User not found")
        updated = user_repo.update_location(db, user, data.latitude, data.longitude)

        try:
            redis_client = get_redis()
            set_user_geo(redis_client, user_id, data.longitude, data.latitude)
            set_user_online(redis_client, user_id)
        except Exception:
            pass

        return _to_user_out(updated)


user_service = UserService()
