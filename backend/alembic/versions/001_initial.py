"""Initial migration

Revision ID: 001
Revises:
Create Date: 2026-01-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('items',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('module', sa.String(length=50), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('title_zh', sa.Text(), server_default=''),
        sa.Column('summary', sa.Text(), server_default=''),
        sa.Column('link', sa.String(length=2048), nullable=False),
        sa.Column('source', sa.String(length=255), server_default=''),
        sa.Column('author', sa.String(length=255), server_default=''),
        sa.Column('pub_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('thumbnail', sa.String(length=2048), server_default=''),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), server_default='[]'),
        sa.Column('fame_score', sa.Integer(), server_default='0'),
        sa.Column('extra', postgresql.JSONB(astext_type=sa.Text()), server_default='{}'),
        sa.Column('core_insight', sa.Text(), server_default=''),
        sa.Column('key_points', postgresql.JSONB(astext_type=sa.Text()), server_default='[]'),
        sa.Column('is_hero', sa.Integer(), server_default='0'),
        sa.Column('fetch_run_id', sa.String(length=36), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_items_module', 'items', ['module'], unique=False)
    op.create_index('ix_items_module_fame', 'items', ['module', sa.text('fame_score DESC')], unique=False)
    op.create_index('ix_items_module_hero', 'items', ['module', 'is_hero'], unique=False)

    op.create_table('fetch_runs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('status', sa.String(length=20), server_default='pending'),
        sa.Column('modules_processed', postgresql.JSONB(astext_type=sa.Text()), server_default='{}'),
        sa.Column('total_items', sa.Integer(), server_default='0'),
        sa.Column('errors', postgresql.JSONB(astext_type=sa.Text()), server_default='[]'),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('fetch_runs')
    op.drop_index('ix_items_module_hero', table_name='items')
    op.drop_index('ix_items_module_fame', table_name='items')
    op.drop_index('ix_items_module', table_name='items')
    op.drop_table('items')
