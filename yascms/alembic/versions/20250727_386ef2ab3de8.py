"""change column name viewable_datetime to display_datetime in news model

Revision ID: 386ef2ab3de8
Revises: 309a6f943d1f
Create Date: 2025-07-27 17:41:48.553662

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '386ef2ab3de8'
down_revision = '309a6f943d1f'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column(
        'news',
        column_name='viewable_datetime',
        new_column_name='display_datetime',
        existing_type=sa.DateTime,
        existing_nullable=False,
    )

def downgrade():
    op.alter_column(
        'news',
        column_name='display_datetime',
        new_column_name='viewable_datetime',
        existing_type=sa.DateTime,
        existing_nullable=False,
    )
