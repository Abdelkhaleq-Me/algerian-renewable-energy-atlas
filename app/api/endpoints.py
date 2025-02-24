# app/api/endpoints.py
import datetime
import requests
from flask import jsonify, request
from flask_restful import Resource
from app.models.energy_models import AlgeriaWelayes, SolarRaster, WindRaster
from app.extensions import db, cache
from sqlalchemy import func

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

class ExternalDataResource(Resource):
    @cache.cached(timeout=3600, query_string=True)
    def get(self):
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        if not lat or not lon:
            return {"error": "lat and lon query parameters are required."}, 400

        current_date = datetime.datetime.now().strftime('%Y%m%d')
        start_date = "20240101"
        base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        community = "RE"

        parameters = [
            ("T2M", "temperature"),
            ("ALLSKY_SFC_SW_DWN", "solar_down"),
            ("WS10M", "wind_10m"),
            ("WS50M", "wind_50m")
        ]

        results = {}
        for param, label in parameters:
            url = (f"{base_url}?community={community}"
                   f"&parameters={param}"
                   f"&latitude={lat}&longitude={lon}"
                   f"&start={start_date}&end={current_date}")
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                results[label] = response.json()
            except requests.RequestException as e:
                results[label] = {"error": f"Failed to fetch data for {param}: {str(e)}"}

        return jsonify(results)
