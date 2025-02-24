# app/api/__init__.py
from flask import Blueprint
from flask_restful import Api
# Import all the Resource classes
from app.api.endpoints import WelayesResource, SolarRasterListResource, WindRasterListResource, ExternalDataResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Add resources to the API here
api.add_resource(WelayesResource, '/welayes')
api.add_resource(SolarRasterListResource, '/solar-rasters')
api.add_resource(WindRasterListResource, '/wind-rasters')
api.add_resource(ExternalDataResource, '/external-data')