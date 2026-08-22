from fastapi import APIRouter

from app.core.exceptions import UnauthorizedError
from app.dependencies import DbSession
from app.schemas.auth import RefreshTokenIn, TokenOut, WechatLoginIn
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/wechat/login", response_model=TokenOut)
async def wechat_login(body: WechatLoginIn, db: DbSession) -> TokenOut:
    return await auth_service.wechat_login(db, body.code)


@router.post("/refresh", response_model=TokenOut)
async def refresh_token(body: RefreshTokenIn) -> TokenOut:
    try:
        return auth_service.refresh_access_token(body.refresh_token)
    except ValueError as exc:
        raise UnauthorizedError(str(exc)) from exc
