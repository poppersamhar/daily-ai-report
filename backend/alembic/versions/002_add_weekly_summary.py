"""Add weekly summaries table

Revision ID: 002
Revises: 001
Create Date: 2026-02-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('weekly_summaries',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('week_start', sa.Date(), nullable=True),
        sa.Column('week_end', sa.Date(), nullable=True),
        sa.Column('headline', sa.Text(), server_default=''),
        sa.Column('hot_topics', postgresql.JSONB(astext_type=sa.Text()), server_default='[]'),
        sa.Column('trend_analysis', sa.Text(), server_default=''),
        sa.Column('key_events', postgresql.JSONB(astext_type=sa.Text()), server_default='[]'),
        sa.Column('company_mentions', postgresql.JSONB(astext_type=sa.Text()), server_default='{}'),
        sa.Column('total_items', sa.Integer(), server_default='0'),
        sa.Column('modules_stats', postgresql.JSONB(astext_type=sa.Text()), server_default='{}'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_weekly_summaries_week_start', 'weekly_summaries', ['week_start'], unique=False)

    # Add index on items.pub_date for date filtering
    op.create_index('ix_items_pub_date', 'items', ['pub_date'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_items_pub_date', table_name='items')
    op.drop_index('ix_weekly_summaries_week_start', table_name='weekly_summaries')
    op.drop_table('weekly_summaries')
