# app/api/__init__.py (Corrected)
from flask import Blueprint
from flask_restful import Api
from app.api.endpoints import (WelayesResource, SolarRasterListResource,
                               WindRasterListResource, ExternalDataResource,
                               RasterDataResource, PointDataResource, BoundaryResource)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(WelayesResource, '/welayes')
api.add_resource(BoundaryResource, '/boundary') # Add BoundaryResource
api.add_resource(SolarRasterListResource, '/solar-rasters')
api.add_resource(WindRasterListResource, '/wind-rasters')
api.add_resource(ExternalDataResource, '/external-data')
api.add_resource(RasterDataResource, '/raster-data')  # Add
api.add_resource(PointDataResource, '/point-data')  # Add
