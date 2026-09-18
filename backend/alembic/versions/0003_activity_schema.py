"""Activity schema

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("creator_id", sa.Integer(), nullable=False),
        sa.Column("region_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("sport_tag_id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("latitude", sa.Numeric(10, 7), nullable=False),
        sa.Column("longitude", sa.Numeric(10, 7), nullable=False),
        sa.Column("address", sa.String(256), nullable=False, server_default=""),
        sa.Column("max_participants", sa.Integer(), nullable=False),
        sa.Column("current_participants", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("gender_requirement", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("registration_deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.SmallInteger(), nullable=False, server_default="1"),
        sa.Column("cover_url", sa.String(512), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["creator_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["sport_tag_id"], ["sport_tags.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_activities_creator_id", "activities", ["creator_id"])
    op.create_index("ix_activities_status", "activities", ["status"])

    op.create_table(
        "activity_participants",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["activity_id"], ["activities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("activity_id", "user_id", name="uq_activity_user"),
    )
    op.create_index("ix_activity_participants_activity_id", "activity_participants", ["activity_id"])
    op.create_index("ix_activity_participants_user_id", "activity_participants", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_activity_participants_user_id", table_name="activity_participants")
    op.drop_index("ix_activity_participants_activity_id", table_name="activity_participants")
    op.drop_table("activity_participants")
    op.drop_index("ix_activities_status", table_name="activities")
    op.drop_index("ix_activities_creator_id", table_name="activities")
    op.drop_table("activities")
