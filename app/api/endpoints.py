# app/api/endpoints.py
import datetime
import requests
from flask import jsonify, request, current_app # Import current_app
from flask_restful import Resource, reqparse
from app.models.energy_models import AlgeriaWelayes, SolarRaster, WindRaster, AlgeriaBoundary
from app.extensions import db, cache
from sqlalchemy import func, text

# No need to create blueprint and api instances here

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

class BoundaryResource(Resource):
    def get(self):
        boundary = AlgeriaBoundary.query.first()  # Assuming you only have one boundary
        if boundary:
             geojson_geom = db.session.scalar(func.ST_AsGeoJSON(boundary.geom))
             return jsonify({
                'id': boundary.id,
                'properties': boundary.properties,
                'geometry': geojson_geom,
            })
        else:
            return jsonify({'message': 'Boundary not found'}), 404 # Return a 404 if no boundary is found


class SolarRasterListResource(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        wilaya_id = request.args.get('wilaya_id', type=int)  # Filter by wilaya
        parameter = request.args.get('parameter', type=str)  # Filter by parameter

        query = SolarRaster.query
        if wilaya_id:
            query = query.filter(SolarRaster.wilaya_id == wilaya_id)
        if parameter:
            query = query.filter(SolarRaster.parameter == parameter)

        rasters = query.paginate(page=page, per_page=per_page, error_out=False)
        results = []
        for raster in rasters.items:
            results.append({
                'id': raster.id,
                'parameter': raster.parameter,
                'resolution': str(raster.resolution) if raster.resolution else None,
                'source': raster.source,
                'acquisition_date': raster.acquisition_date.isoformat() if raster.acquisition_date else None,
                'wilaya_id': raster.wilaya_id  # Include wilaya_id in the response
            })
        return jsonify({
            'total': rasters.total,
            'page': rasters.page,
            'per_page': rasters.per_page,
            'items': results
        })

class WindRasterListResource(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        wilaya_id = request.args.get('wilaya_id', type=int)
        parameter = request.args.get('parameter', type=str)
        altitude = request.args.get('altitude', type=int)

        query = WindRaster.query
        if wilaya_id:
            query = query.filter(WindRaster.wilaya_id == wilaya_id)
        if parameter:
            query = query.filter(WindRaster.parameter == parameter)
        if altitude:
            query = query.filter(WindRaster.altitude == altitude)


        rasters = query.paginate(page=page, per_page=per_page, error_out=False)
        results = []
        for raster in rasters.items:
            results.append({
                'id': raster.id,
                'parameter': raster.parameter,
                'altitude': raster.altitude,
                'resolution': str(raster.resolution) if raster.resolution else None,
                'source': raster.source,
                'acquisition_date': raster.acquisition_date.isoformat() if raster.acquisition_date else None,
                'wilaya_id': raster.wilaya_id
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
        parser.add_argument('parameters', type=str, action='append', help="List of parameters (e.g., T2M)")
        args = parser.parse_args()

        end_date = args['end_date'] or datetime.datetime.now().strftime('%Y%m%d')
        start_date = args['start_date'] or "20240101"  # Good default

        try:
            datetime.datetime.strptime(start_date, '%Y%m%d')
            datetime.datetime.strptime(end_date, '%Y%m%d')
        except ValueError:
            return {"error": "Invalid date format. Use YYYYMMDD."}, 400

        base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        community = "RE"

        requested_parameters = args['parameters'] or ['T2M']

        results = {}
        for param in requested_parameters:
            label = {
                'T2M': 'temperature_2m',
                'ALLSKY_SFC_SW_DWN': 'solar_down',
                'WS10M': 'wind_10m',
                'WS50M': 'wind_50m'
            }.get(param, param)

            url = (f"{base_url}?community={community}"
                   f"¶meters={param}"  # Corrected parameter pluralization
                   f"&latitude={args['lat']}&longitude={args['lon']}"
                   f"&start={start_date}&end={end_date}&format=json") # Add format=json

            try:
                current_app.logger.info(f"Fetching data from: {url}") # Log the URL
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # This is good - raises HTTPError for bad codes
                data = response.json()
                # Extract the data you need, handling potential key errors
                if 'features' in data and len(data['features']) > 0:
                    properties = data['features'][0].get('properties')
                    if properties and param in properties:
                        results[label] = properties[param]
                    else:
                        results[label] = {"error": f"Parameter '{param}' not found in response."}
                else:
                    results[label] = {"error": "No data returned from API."}


            except requests.exceptions.RequestException as e:
                error_message = f"Request failed: {str(e)}" # Simplified error message
                results[label] = {"error": error_message}
                current_app.logger.error(error_message)


        return jsonify(results)


class RasterDataResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('layer_type', type=str, required=True,
                            help="Layer type is required (solar or wind)")
        parser.add_argument('parameter', type=str, required=True,
                            help="Parameter is required")
        parser.add_argument('wilaya_id', type=int, required=True,
                            help="Wilaya ID is required")
        parser.add_argument('date', type=str,
                            help="Date for the raster (YYYY-MM-DD)")  # Optional date
        args = parser.parse_args()

        layer_type = args['layer_type'].lower()
        if layer_type not in ['solar', 'wind']:
            return {'message': 'Invalid layer type. Choose "solar" or "wind".'}, 400

        wilaya_id = args['wilaya_id']
        parameter = args['parameter']

        try:  # Added try-except block
            date = datetime.datetime.strptime(args['date'], '%Y-%m-%d').date() if args['date'] else None
        except ValueError:
            return {"message": "Invalid date format.  Use YYYY-MM-DD."}, 400

        if layer_type == 'solar':
            query = SolarRaster.query.filter(
                SolarRaster.wilaya_id == wilaya_id,
                SolarRaster.parameter == parameter
            )
            if date:
                query = query.filter(SolarRaster.acquisition_date == date)

        elif layer_type == 'wind':
            query = WindRaster.query.filter(
                WindRaster.wilaya_id == wilaya_id,
                WindRaster.parameter == parameter
            )
            if date:
                query = query.filter(WindRaster.acquisition_date == date)

        raster_entry = query.first()

        if not raster_entry:
            return {'message': 'Raster data not found for the specified criteria.'}, 404

        # Get raster statistics (you might want to cache these)
        stats = db.session.query(
           func.ST_SummaryStats(raster_entry.rast, 1, True)  # Assuming band 1, with nodata handling
        ).first()

        if stats and stats[0]:  # Check if stats were returned
            stats_dict = {
                'count': stats[0][0],
                'sum': stats[0][1],
                'mean': stats[0][2],
                'stddev': stats[0][3],
                'min': stats[0][4],
                'max': stats[0][5]
            }
        else:
            stats_dict = {'message': 'Could not compute raster statistics.'}

        return jsonify({
            'id': raster_entry.id,
            'parameter': raster_entry.parameter,
            'wilaya_id': raster_entry.wilaya_id,
            'acquisition_date': raster_entry.acquisition_date.isoformat() if raster_entry.acquisition_date else None,
            'statistics': stats_dict
        })


class PointDataResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('lat', type=float, required=True, help="Latitude is required")
        parser.add_argument('lon', type=float, required=True, help="Longitude is required")
        parser.add_argument('layer_type', type=str, required=True,
                            help="Layer type is required (solar or wind)")
        parser.add_argument('parameter', type=str, required=True,
                            help="Parameter is required")
        parser.add_argument('date', type=str,
                            help="Date for the raster (YYYY-MM-DD)")  # Optional date

        args = parser.parse_args()
        lat = args['lat']
        lon = args['lon']
        layer_type = args['layer_type'].lower()
        parameter = args['parameter']

        if layer_type not in ['solar', 'wind']:
            return {'message': 'Invalid layer type. Choose "solar" or "wind".'}, 400

        try:
            date = datetime.datetime.strptime(args['date'], '%Y-%m-%d').date() if args['date'] else None
        except ValueError:
            return {"message": "Invalid date format.  Use YYYY-MM-DD."}, 400

        point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)

        if layer_type == 'solar':
            query = SolarRaster.query.filter(
                SolarRaster.parameter == parameter,
                func.ST_Intersects(SolarRaster.rast, point)
            )
            if date:
                query = query.filter(SolarRaster.acquisition_date == date)

        elif layer_type == 'wind':
            query = WindRaster.query.filter(
                WindRaster.parameter == parameter,
                func.ST_Intersects(WindRaster.rast, point)
            )
            if date:
                query = query.filter(WindRaster.acquisition_date == date)


        raster_entry = query.first()

        if not raster_entry:
            return {'message': 'Raster data not found for the specified location and criteria.'}, 404


        # Extract the value at the point
        value = db.session.scalar(
            func.ST_Value(raster_entry.rast, 1, point) # Band 1
        )

        return jsonify({
            'latitude': lat,
            'longitude': lon,
            'parameter': raster_entry.parameter,
            'date': raster_entry.acquisition_date.isoformat() if raster_entry.acquisition_date else None,
            'value': value
        })
