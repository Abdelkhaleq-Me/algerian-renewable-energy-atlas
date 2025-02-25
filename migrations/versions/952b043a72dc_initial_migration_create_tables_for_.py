"""Initial migration: create tables for spatial data

Revision ID: 952b043a72dc
Revises: 7babb588c434
Create Date: 2025-02-25 13:20:19.185633
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '952b043a72dc'
down_revision = '7babb588c434'
branch_labels = None
depends_on = None

def upgrade():
    # Do nothing here because spatial_ref_sys is managed by PostGIS and should not be dropped.
    pass

def downgrade():
    # Do nothing here as well.
    pass
