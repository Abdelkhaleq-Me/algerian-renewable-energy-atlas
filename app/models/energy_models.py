from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry, Raster
from app.extensions import db

class AlgeriaWelayes(db.Model):
    __tablename__ = 'algeria_welayes'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    properties = Column(JSONB)
    # Storing multipolygon geometry for administrative regions
    geom = Column(Geometry('MULTIPOLYGON', srid=4326))

    def __repr__(self):
        return f"<AlgeriaWelayes(id={self.id}, name='{self.name}')>"

class AlgeriaBoundary(db.Model):
    __tablename__ = 'algeria_boundary'
    id = Column(Integer, primary_key=True)
    properties = Column(JSONB)
    # Storing the country boundary (polygon or multipolygon)
    geom = Column(Geometry('POLYGON', srid=4326))

    def __repr__(self):
        return f"<AlgeriaBoundary(id={self.id})>"

class SolarRaster(db.Model):
    __tablename__ = 'solar_rasters'
    id = Column(Integer, primary_key=True)
    parameter = Column(String(50), nullable=False)  # e.g., 'GHI', 'DNI', etc.
    rast = Column(Raster)  # The raster data from GeoTIFF
    resolution = Column(Numeric, nullable=True)
    source = Column(String(255), nullable=True)
    acquisition_date = Column(Date, nullable=True)

    def __repr__(self):
        return f"<SolarRaster(id={self.id}, parameter='{self.parameter}')>"

class WindRaster(db.Model):
    __tablename__ = 'wind_rasters'
    id = Column(Integer, primary_key=True)
    parameter = Column(String(50), nullable=False)  # e.g., 'wind-speed_10m', etc.
    rast = Column(Raster)
    altitude = Column(Integer, nullable=False)  # e.g., 10, 50, 100, etc.
    resolution = Column(Numeric, nullable=True)
    source = Column(String(255), nullable=True)
    acquisition_date = Column(Date, nullable=True)

    def __repr__(self):
        return f"<WindRaster(id={self.id}, parameter='{self.parameter}', altitude={self.altitude})>"
