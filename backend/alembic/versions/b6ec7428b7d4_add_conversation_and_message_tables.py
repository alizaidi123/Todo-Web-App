"""Add conversation and message tables

Revision ID: b6ec7428b7d4
Revises: 
Create Date: 2026-01-25 13:05:47.689453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6ec7428b7d4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create conversation table
    op.create_table(
        'conversation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    # Create index separately to avoid issues
    op.create_index('ix_conversation_user_id', 'conversation', ['user_id'])

    # Create message table
    op.create_table(
        'message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.Enum('user', 'assistant', 'system', name='messagerole'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', sa.Text(), nullable=True),
        sa.Column('tool_responses', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # Create index separately to avoid issues
    op.create_index('ix_message_conversation_id', 'message', ['conversation_id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop message table first (due to foreign key constraint)
    op.drop_table('message')

    # Drop conversation table
    op.drop_table('conversation')

    # Drop the enum type
    op.execute("DROP TYPE IF EXISTS messagerole")
