# app/models/energy_models.py (Corrected)
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry, Raster
from geoalchemy2.shape import to_shape
from shapely.geometry import MultiPolygon
from app.extensions import db

class AlgeriaWelayes(db.Model):
    __tablename__ = 'algeria_welayes'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    properties = Column(JSONB)
    geom = Column(Geometry('MULTIPOLYGON', srid=4326), index=True)

    # Relationships (for easier querying later)
    solar_rasters = relationship('SolarRaster', backref='wilaya', lazy=True)
    wind_rasters = relationship('WindRaster', backref='wilaya', lazy=True)

    def __repr__(self):
        return f"<AlgeriaWelayes(id={self.id}, name='{self.name}')>"

    @property
    def shape(self):
        """Converts the geom (WKBElement) to a Shapely object for easier manipulation."""
        return to_shape(self.geom)

class AlgeriaBoundary(db.Model):
    __tablename__ = 'algeria_boundary'
    id = Column(Integer, primary_key=True)
    properties = Column(JSONB)
    geom = Column(Geometry('POLYGON', srid=4326), index=True) # Changed to POLYGON

    def __repr__(self):
        return f"<AlgeriaBoundary(id={self.id})>"

    @property
    def shape(self):
        """Converts the geom (WKBElement) to a Shapely object."""
        return to_shape(self.geom)

class SolarRaster(db.Model):
    __tablename__ = 'solar_rasters'
    id = Column(Integer, primary_key=True)
    parameter = Column(String(50), nullable=False, index=True)  # e.g., 'GHI', 'DNI'
    rast = Column(Raster)
    resolution = Column(Numeric, nullable=True)
    source = Column(String(255), nullable=True)
    acquisition_date = Column(Date, nullable=True, index=True)
    wilaya_id = Column(Integer, ForeignKey('algeria_welayes.id'), nullable=True, index=True)


    def __repr__(self):
        return f"<SolarRaster(id={self.id}, parameter='{self.parameter}')>"

class WindRaster(db.Model):
    __tablename__ = 'wind_rasters'
    id = Column(Integer, primary_key=True)
    parameter = Column(String(50), nullable=False, index=True)  # e.g., 'wind-speed_10m'
    rast = Column(Raster)
    altitude = Column(Integer, nullable=False, index=True)  # e.g., 10, 50, 100
    resolution = Column(Numeric, nullable=True)
    source = Column(String(255), nullable=True)
    acquisition_date = Column(Date, nullable=True, index=True)
    wilaya_id = Column(Integer, ForeignKey('algeria_welayes.id'), nullable=True, index=True)

    def __repr__(self):
        return f"<WindRaster(id={self.id}, parameter='{self.parameter}', altitude={self.altitude})>"