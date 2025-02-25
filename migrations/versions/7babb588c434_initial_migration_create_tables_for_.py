"""Initial migration: create tables for spatial data

Revision ID: 7babb588c434
Revises: 
Create Date: 2025-02-25 11:59:38.603857

"""
from alembic import op
import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7babb588c434'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create algeria_boundary table
    op.create_table(
        'algeria_boundary',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('properties', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('geom', geoalchemy2.types.Geometry(
            geometry_type='POLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # Instead of indexing the full geometry, index its envelope:
    op.execute("DROP INDEX IF EXISTS idx_algeria_boundary_geom;")
    with op.batch_alter_table('algeria_boundary', schema=None) as batch_op:
        batch_op.create_index('idx_algeria_boundary_geom_envelope', [sa.text('ST_Envelope(geom)')], unique=False, postgresql_using='gist')

    # Create algeria_welayes table
    op.create_table(
        'algeria_welayes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('properties', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('geom', geoalchemy2.types.Geometry(
            geometry_type='MULTIPOLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # Index the envelope of the geometry to avoid overly large index rows
    op.execute("DROP INDEX IF EXISTS idx_algeria_welayes_geom;")
    with op.batch_alter_table('algeria_welayes', schema=None) as batch_op:
        batch_op.create_index('idx_algeria_welayes_geom_envelope', [sa.text('ST_Envelope(geom)')], unique=False, postgresql_using='gist')

    # Create solar_rasters table (unchanged)
    op.create_table(
        'solar_rasters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('parameter', sa.String(length=50), nullable=False),
        sa.Column('rast', geoalchemy2.types.Raster(from_text='raster', name='raster'), nullable=True),
        sa.Column('resolution', sa.Numeric(), nullable=True),
        sa.Column('source', sa.String(length=255), nullable=True),
        sa.Column('acquisition_date', sa.Date(), nullable=True),
        sa.Column('wilaya_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['wilaya_id'], ['algeria_welayes.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.execute("DROP INDEX IF EXISTS idx_solar_rasters_rast;")
    with op.batch_alter_table('solar_rasters', schema=None) as batch_op:
        batch_op.create_index('idx_solar_rasters_rast', [sa.text('ST_ConvexHull(rast)')],
                              unique=False, postgresql_using='gist')
        batch_op.create_index(batch_op.f('ix_solar_rasters_acquisition_date'), ['acquisition_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_solar_rasters_parameter'), ['parameter'], unique=False)
        batch_op.create_index(batch_op.f('ix_solar_rasters_wilaya_id'), ['wilaya_id'], unique=False)

    # Create wind_rasters table (unchanged)
    op.create_table(
        'wind_rasters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('parameter', sa.String(length=50), nullable=False),
        sa.Column('rast', geoalchemy2.types.Raster(from_text='raster', name='raster'), nullable=True),
        sa.Column('altitude', sa.Integer(), nullable=False),
        sa.Column('resolution', sa.Numeric(), nullable=True),
        sa.Column('source', sa.String(length=255), nullable=True),
        sa.Column('acquisition_date', sa.Date(), nullable=True),
        sa.Column('wilaya_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['wilaya_id'], ['algeria_welayes.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.execute("DROP INDEX IF EXISTS idx_wind_rasters_rast;")
    with op.batch_alter_table('wind_rasters', schema=None) as batch_op:
        batch_op.create_index('idx_wind_rasters_rast', [sa.text('ST_ConvexHull(rast)')],
                              unique=False, postgresql_using='gist')
        batch_op.create_index(batch_op.f('ix_wind_rasters_acquisition_date'), ['acquisition_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_wind_rasters_altitude'), ['altitude'], unique=False)
        batch_op.create_index(batch_op.f('ix_wind_rasters_parameter'), ['parameter'], unique=False)
        batch_op.create_index(batch_op.f('ix_wind_rasters_wilaya_id'), ['wilaya_id'], unique=False)

    # Do not drop spatial_ref_sys because it is managed by PostGIS
    # op.drop_table('spatial_ref_sys')


def downgrade():
    with op.batch_alter_table('wind_rasters', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_wind_rasters_wilaya_id'))
        batch_op.drop_index(batch_op.f('ix_wind_rasters_parameter'))
        batch_op.drop_index(batch_op.f('ix_wind_rasters_altitude'))
        batch_op.drop_index(batch_op.f('ix_wind_rasters_acquisition_date'))
        batch_op.drop_index('idx_wind_rasters_rast', postgresql_using='gist')
    op.drop_table('wind_rasters')
    with op.batch_alter_table('solar_rasters', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_solar_rasters_wilaya_id'))
        batch_op.drop_index(batch_op.f('ix_solar_rasters_parameter'))
        batch_op.drop_index(batch_op.f('ix_solar_rasters_acquisition_date'))
        batch_op.drop_index('idx_solar_rasters_rast', postgresql_using='gist')
    op.drop_table('solar_rasters')
    with op.batch_alter_table('algeria_welayes', schema=None) as batch_op:
        batch_op.drop_index('idx_algeria_welayes_geom_envelope', postgresql_using='gist')
        batch_op.drop_index(batch_op.f('ix_algeria_welayes_geom'))
    op.drop_table('algeria_welayes')
    with op.batch_alter_table('algeria_boundary', schema=None) as batch_op:
        batch_op.drop_index('idx_algeria_boundary_geom_envelope', postgresql_using='gist')
        batch_op.drop_index(batch_op.f('ix_algeria_boundary_geom'))
    op.drop_table('algeria_boundary')
