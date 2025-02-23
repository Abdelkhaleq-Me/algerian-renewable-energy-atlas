# app/__init__.py

from flask import Flask
from app import config
from app.extensions import db, babel, cache, init_app as init_extensions
from app.routes.home import home_bp
from app.routes.atlas import atlas_bp
from app.routes.download import download_bp
from app.routes.about import about_bp
from app.api.endpoints import api_bp


def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)

    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(atlas_bp)
    app.register_blueprint(download_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(api_bp, url_prefix='/api') # Example url prefix for API

    return app