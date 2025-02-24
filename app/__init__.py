# app/__init__.py
from flask import Flask
from app.config import DevelopmentConfig
from app.extensions import init_app as init_extensions
from app.routes import init_app as init_routes
from app.api.endpoints import api_bp  # Import your API blueprint

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    init_extensions(app)
    
    # Register routes
    init_routes(app)

    # Register API blueprint with a URL prefix
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

