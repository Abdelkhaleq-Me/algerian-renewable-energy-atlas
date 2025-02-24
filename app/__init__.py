#app/__init__.py
from flask import Flask
from app.config import DevelopmentConfig  # Or ProductionConfig
from app.extensions import init_app as init_extensions
from app.routes import init_app as init_routes
from app.api import api_bp #Import api_bp

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)
    init_routes(app)
    app.register_blueprint(api_bp, url_prefix='/api') #Register the blueprint

    return app
