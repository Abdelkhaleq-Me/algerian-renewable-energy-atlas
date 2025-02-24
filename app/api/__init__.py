# app/api/__init__.py
from flask import Blueprint
from flask_restful import Api
from app.api.endpoints import WelayesResource, SolarRasterResource, WindRasterResource, ExternalDataResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(WelayesResource, '/welayes')
api.add_resource(SolarRasterResource, '/solar_rasters')
api.add_resource(WindRasterResource, '/wind_rasters')
api.add_resource(ExternalDataResource, '/external_data')

