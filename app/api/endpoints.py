# app/api/endpoints.py
from flask import jsonify
from flask_restful import Resource, Api
from app.models.energy_models import AlgeriaWelayes, SolarRaster, WindRaster
from app.extensions import db
from sqlalchemy import func

# Assuming you have created a Blueprint for your API (api_bp)
api = Api()

class WelayesResource(Resource):
    def get(self):
        welayes = AlgeriaWelayes.query.all()
        results = []
        for welaya in welayes:
            geojson_geom = db.session.scalar(func.ST_AsGeoJSON(welaya.geom))
            results.append({
                'id': welaya.id,
                'name': welaya.name,
                'properties': welaya.properties,
                'geometry': geojson_geom
            })
        return jsonify(results)

class SolarRasterResource(Resource):
    def get(self):
        rasters = SolarRaster.query.all()
        results = []
        for raster in rasters:
            results.append({
                'id': raster.id,
                'parameter': raster.parameter,
                'resolution': str(raster.resolution) if raster.resolution else None,
                'source': raster.source,
                'acquisition_date': raster.acquisition_date.isoformat() if raster.acquisition_date else None
            })
        return jsonify(results)

class WindRasterResource(Resource):
    def get(self):
        rasters = WindRaster.query.all()
        results = []
        for raster in rasters:
            results.append({
                'id': raster.id,
                'parameter': raster.parameter,
                'altitude': raster.altitude,
                'resolution': str(raster.resolution) if raster.resolution else None,
                'source': raster.source,
                'acquisition_date': raster.acquisition_date.isoformat() if raster.acquisition_date else None
            })
        return jsonify(results)

# Register the resources with the API
api.add_resource(WelayesResource, '/welayes')
api.add_resource(SolarRasterResource, '/solar_rasters')
api.add_resource(WindRasterResource, '/wind_rasters')
