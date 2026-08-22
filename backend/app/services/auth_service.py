from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, decode_token
from app.repositories.user_repo import user_repo
from app.schemas.auth import TokenOut
from app.services.wechat_service import code2session


class AuthService:
    async def wechat_login(self, db: Session, code: str) -> TokenOut:
        session = await code2session(code)
        user = user_repo.get_by_openid(db, session.openid)
        is_new_user = user is None

        if user is None:
            user = user_repo.create(db, openid=session.openid, unionid=session.unionid)
        elif session.unionid and not user.unionid:
            user.unionid = session.unionid
            db.commit()

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return TokenOut(
            access_token=access_token,
            refresh_token=refresh_token,
            is_new_user=is_new_user,
        )

    def refresh_access_token(self, refresh_token: str) -> TokenOut:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")
        user_id = payload["sub"]
        return TokenOut(
            access_token=create_access_token(user_id),
            refresh_token=create_refresh_token(user_id),
        )


auth_service = AuthService()
