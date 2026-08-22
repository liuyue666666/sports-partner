import hashlib
import logging

import httpx

from app.config import settings
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)

WECHAT_CODE2SESSION_URL = "https://api.weixin.qq.com/sns/jscode2session"


class WechatSession:
    def __init__(self, openid: str, session_key: str, unionid: str | None = None) -> None:
        self.openid = openid
        self.session_key = session_key
        self.unionid = unionid


async def code2session(code: str) -> WechatSession:
    if not settings.wechat_app_id or not settings.wechat_app_secret:
        logger.warning("WeChat credentials not configured, using dev mock login")
        openid = f"dev_{hashlib.sha256(code.encode()).hexdigest()[:28]}"
        return WechatSession(openid=openid, session_key="dev_session")

    params = {
        "appid": settings.wechat_app_id,
        "secret": settings.wechat_app_secret,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(WECHAT_CODE2SESSION_URL, params=params)
        data = response.json()

    if data.get("errcode"):
        raise AppException(
            message=data.get("errmsg", "WeChat login failed"),
            code="WECHAT_LOGIN_FAILED",
            status_code=400,
            detail={"errcode": data.get("errcode")},
        )

    return WechatSession(
        openid=data["openid"],
        session_key=data.get("session_key", ""),
        unionid=data.get("unionid"),
    )
