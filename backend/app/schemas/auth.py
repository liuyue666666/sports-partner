from pydantic import BaseModel, Field


class WechatLoginIn(BaseModel):
    code: str = Field(min_length=1, max_length=128)


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    is_new_user: bool = False


class RefreshTokenIn(BaseModel):
    refresh_token: str
