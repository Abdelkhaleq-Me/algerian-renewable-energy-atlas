# app/api/endpoints.py
import datetime
import requests
from flask import jsonify, request
from flask_restful import Resource, reqparse # Import reqparse
from app.models.energy_models import AlgeriaWelayes, SolarRaster, WindRaster
from app.extensions import db, cache
from sqlalchemy import func

#No need to create blueprint and api instances here

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

class SolarRasterListResource(Resource):  # Renamed for clarity
    def get(self):
        # Use pagination to limit the number of results
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)  # Default to 20

        rasters = SolarRaster.query.paginate(page=page, per_page=per_page, error_out=False)
        results = []
        for raster in rasters.items:
            results.append({
                'id': raster.id,
                'parameter': raster.parameter,
                'resolution': str(raster.resolution) if raster.resolution else None,
                'source': raster.source,
                'acquisition_date': raster.acquisition_date.isoformat() if raster.acquisition_date else None
            })
        return jsonify({
            'total': rasters.total,
            'page': rasters.page,
            'per_page': rasters.per_page,
            'items': results
        })

class WindRasterListResource(Resource):  # Renamed for clarity
    def get(self):
        # Use pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        rasters = WindRaster.query.paginate(page=page, per_page=per_page, error_out=False)
        results = []
        for raster in rasters.items:
            results.append({
                'id': raster.id,
                'parameter': raster.parameter,
                'altitude': raster.altitude,
                'resolution': str(raster.resolution) if raster.resolution else None,
                'source': raster.source,
                'acquisition_date': raster.acquisition_date.isoformat() if raster.acquisition_date else None
            })
        return jsonify({
            'total': rasters.total,
            'page': rasters.page,
            'per_page': rasters.per_page,
            'items': results
        })

class ExternalDataResource(Resource):
    @cache.cached(timeout=3600, query_string=True)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('lat', type=float, required=True, help="Latitude is required")
        parser.add_argument('lon', type=float, required=True, help="Longitude is required")
        parser.add_argument('start_date', type=str, help="Start date (YYYYMMDD)")
        parser.add_argument('end_date', type=str, help="End date (YYYYMMDD)")
        parser.add_argument('parameters', type=str, action='append', help="List of parameters (e.g., T2M)") #NEW
        args = parser.parse_args()

        end_date = args['end_date'] or datetime.datetime.now().strftime('%Y%m%d')
        start_date = args['start_date'] or "20240101"

        try:
            datetime.datetime.strptime(start_date, '%Y%m%d')
            datetime.datetime.strptime(end_date, '%Y%m%d')
        except ValueError:
            return {"error": "Invalid date format. Use YYYYMMDD."}, 400

        base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        community = "RE"

        # Use the provided parameters, or default to T2M if none are specified
        requested_parameters = args['parameters'] or ['T2M'] #NEW

        results = {}
        for param in requested_parameters: #NEW - Iterate through requested params
            # Map API parameter names to more descriptive labels (optional)
            label = {
                'T2M': 'temperature_2m',
                'ALLSKY_SFC_SW_DWN': 'solar_down',
                'WS10M': 'wind_10m',
                'WS50M': 'wind_50m'
            }.get(param, param) # Use .get() for safety


            url = (f"{base_url}?community={community}"
                   f"¶meters={param}"  # Only request the specific parameter
                   f"&latitude={args['lat']}&longitude={args['lon']}"
                   f"&start={start_date}&end={end_date}")

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                results[label] = response.json() #Store results using descriptive labels
            except requests.exceptions.RequestException as e:
                if isinstance(e, requests.exceptions.Timeout):
                    error_message = f"Timeout error fetching data for {param}."
                elif isinstance(e, requests.exceptions.HTTPError):
                    error_message = f"HTTP error ({e.response.status_code}) fetching data for {param}."
                else:
                    error_message = f"Failed to fetch data for {param}: {str(e)}"
                results[label] = {"error": error_message}
                db.get_app().logger.error(error_message)

        return jsonify(results)
