"""Initial schema placeholder

Revision ID: 0001
Revises:
Create Date: 2026-08-03

Phase 0 skeleton — no tables yet. User/activity tables added in Phase 1+.
"""

from typing import Sequence, Union

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
