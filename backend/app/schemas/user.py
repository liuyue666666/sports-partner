from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel, Field, field_validator


class GenderEnum(IntEnum):
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2


class SportTagOut(BaseModel):
    id: int
    name: str
    icon: str
    sort_order: int

    model_config = {"from_attributes": True}


class UserOut(BaseModel):
    id: int
    nickname: str
    avatar_url: str
    gender: GenderEnum
    bio: str
    latitude: float | None = None
    longitude: float | None = None
    location_updated_at: datetime | None = None
    available_start: datetime | None = None
    available_end: datetime | None = None
    sport_tags: list[SportTagOut] = Field(default_factory=list)
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("latitude", "longitude", mode="before")
    @classmethod
    def coerce_decimal(cls, value):
        if value is None:
            return None
        return float(value)


class UserPublicOut(BaseModel):
    id: int
    nickname: str
    avatar_url: str
    gender: GenderEnum
    bio: str
    sport_tags: list[SportTagOut] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class UserUpdateIn(BaseModel):
    nickname: str | None = Field(default=None, max_length=64)
    avatar_url: str | None = Field(default=None, max_length=512)
    gender: GenderEnum | None = None
    bio: str | None = Field(default=None, max_length=256)
    sport_tag_ids: list[int] | None = None
    available_start: datetime | None = None
    available_end: datetime | None = None


class LocationUpdateIn(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
