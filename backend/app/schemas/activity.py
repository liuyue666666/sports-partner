from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel, Field, field_validator

from app.schemas.user import SportTagOut, UserPublicOut


class ActivityStatusEnum(IntEnum):
    RECRUITING = 1
    FULL = 2
    IN_PROGRESS = 3
    ENDED = 4
    CANCELLED = 5


class GenderRequirementEnum(IntEnum):
    ANY = 0
    MALE_ONLY = 1
    FEMALE_ONLY = 2


class ActivityCreateIn(BaseModel):
    title: str = Field(min_length=1, max_length=128)
    description: str = Field(default="", max_length=5000)
    sport_tag_id: int
    start_time: datetime
    end_time: datetime | None = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    address: str = Field(default="", max_length=256)
    max_participants: int = Field(ge=2, le=100)
    gender_requirement: GenderRequirementEnum = GenderRequirementEnum.ANY
    registration_deadline: datetime
    cover_url: str = Field(default="", max_length=512)

    @field_validator("registration_deadline")
    @classmethod
    def deadline_before_start(cls, v: datetime, info) -> datetime:
        start = info.data.get("start_time")
        if start and v > start:
            raise ValueError("registration_deadline must be before start_time")
        return v


class ParticipantOut(BaseModel):
    user: UserPublicOut
    joined_at: datetime

    model_config = {"from_attributes": True}


class ActivityOut(BaseModel):
    id: int
    title: str
    description: str
    sport_tag: SportTagOut
    start_time: datetime
    end_time: datetime | None = None
    latitude: float
    longitude: float
    address: str
    max_participants: int
    current_participants: int
    gender_requirement: GenderRequirementEnum
    registration_deadline: datetime
    status: ActivityStatusEnum
    cover_url: str
    creator: UserPublicOut
    distance_meters: float | None = None
    is_joined: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("latitude", "longitude", mode="before")
    @classmethod
    def coerce_decimal(cls, value):
        return float(value) if value is not None else value


class ActivityDetailOut(ActivityOut):
    participants: list[ParticipantOut] = Field(default_factory=list)
