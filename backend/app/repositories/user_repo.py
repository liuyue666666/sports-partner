from datetime import datetime, timezone

from sqlalchemy.orm import Session, selectinload

from app.models.user import SportTag, User, UserStatus
from app.schemas.user import UserUpdateIn


class UserRepository:
    def get_by_id(self, db: Session, user_id: int) -> User | None:
        return (
            db.query(User)
            .options(selectinload(User.sport_tags))
            .filter(User.id == user_id, User.status == UserStatus.ACTIVE.value)
            .first()
        )

    def get_by_openid(self, db: Session, openid: str) -> User | None:
        return db.query(User).filter(User.openid == openid).first()

    def create(self, db: Session, *, openid: str, unionid: str | None = None) -> User:
        user = User(openid=openid, unionid=unionid, nickname="运动达人")
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update_profile(self, db: Session, user: User, data: UserUpdateIn) -> User:
        if data.nickname is not None:
            user.nickname = data.nickname
        if data.avatar_url is not None:
            user.avatar_url = data.avatar_url
        if data.gender is not None:
            user.gender = int(data.gender)
        if data.bio is not None:
            user.bio = data.bio
        if data.available_start is not None:
            user.available_start = data.available_start
        if data.available_end is not None:
            user.available_end = data.available_end

        if data.sport_tag_ids is not None:
            tags = db.query(SportTag).filter(SportTag.id.in_(data.sport_tag_ids)).all()
            user.sport_tags = tags

        db.commit()
        db.refresh(user)
        return self.get_by_id(db, user.id) or user

    def update_location(self, db: Session, user: User, latitude: float, longitude: float) -> User:
        user.latitude = latitude
        user.longitude = longitude
        user.location_updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
        return user

    def list_sport_tags(self, db: Session) -> list[SportTag]:
        return db.query(SportTag).order_by(SportTag.sort_order).all()


user_repo = UserRepository()
