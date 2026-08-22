from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import UnauthorizedError
from app.core.security import decode_token
from app.models.user import User, UserStatus
from app.repositories.user_repo import user_repo

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user_id(authorization: Annotated[str | None, Header()] = None) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Missing or invalid authorization header")
    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = decode_token(token)
    except ValueError as exc:
        raise UnauthorizedError("Invalid or expired token") from exc
    if payload.get("type") != "access":
        raise UnauthorizedError("Invalid token type")
    return int(payload["sub"])


def get_current_user(
    db: DbSession,
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> User:
    user = user_repo.get_by_id(db, user_id)
    if not user or user.status != UserStatus.ACTIVE.value:
        raise UnauthorizedError("User not found or disabled")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentUserId = Annotated[int, Depends(get_current_user_id)]
