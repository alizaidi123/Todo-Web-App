"""Convert priority column from INTEGER to TEXT with string values

Revision ID: 87833a57b8d1
Revises: c22dced079a6
Create Date: 2026-01-30 10:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer


# revision identifiers, used by Alembic.
revision: str = '87833a57b8d1'
down_revision: Union[str, Sequence[str], None] = 'c22dced079a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Convert INTEGER column to TEXT using USING clause for atomic conversion
    # This safely maps values: 1 -> 'low', 2 -> 'medium', 3 -> 'high', others -> 'medium'
    op.execute("""
        ALTER TABLE task
        ALTER COLUMN priority TYPE TEXT
        USING (
            CASE
                WHEN priority = 1 THEN 'low'
                WHEN priority = 2 THEN 'medium'
                WHEN priority = 3 THEN 'high'
                ELSE 'medium'
            END
        )
    """)


def downgrade() -> None:
    # Convert TEXT column back to INTEGER using USING clause for atomic conversion
    # This safely maps values: 'low' -> 1, 'medium' -> 2, 'high' -> 3, others -> 2
    op.execute("""
        ALTER TABLE task
        ALTER COLUMN priority TYPE INTEGER
        USING (
            CASE
                WHEN priority = 'low' THEN 1
                WHEN priority = 'medium' THEN 2
                WHEN priority = 'high' THEN 3
                ELSE 2
            END
        )
    """)