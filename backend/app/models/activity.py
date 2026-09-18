import enum
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ActivityStatus(int, enum.Enum):
    RECRUITING = 1
    FULL = 2
    IN_PROGRESS = 3
    ENDED = 4
    CANCELLED = 5


class GenderRequirement(int, enum.Enum):
    ANY = 0
    MALE_ONLY = 1
    FEMALE_ONLY = 2


class ParticipantStatus(int, enum.Enum):
    JOINED = 0
    CANCELLED = 1


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    region_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    sport_tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("sport_tags.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    latitude: Mapped[float] = mapped_column(Numeric(10, 7), nullable=False)
    longitude: Mapped[float] = mapped_column(Numeric(10, 7), nullable=False)
    address: Mapped[str] = mapped_column(String(256), default="", nullable=False)
    max_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    current_participants: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    gender_requirement: Mapped[int] = mapped_column(
        SmallInteger, default=GenderRequirement.ANY.value, nullable=False
    )
    registration_deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[int] = mapped_column(
        SmallInteger, default=ActivityStatus.RECRUITING.value, nullable=False, index=True
    )
    cover_url: Mapped[str] = mapped_column(String(512), default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    creator: Mapped["User"] = relationship("User", foreign_keys=[creator_id])
    sport_tag: Mapped["SportTag"] = relationship("SportTag")
    participants: Mapped[list["ActivityParticipant"]] = relationship(
        back_populates="activity",
        cascade="all, delete-orphan",
    )


class ActivityParticipant(Base):
    __tablename__ = "activity_participants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    activity_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status: Mapped[int] = mapped_column(SmallInteger, default=ParticipantStatus.JOINED.value, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    activity: Mapped[Activity] = relationship(back_populates="participants")
    user: Mapped["User"] = relationship("User")


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import SportTag, User
