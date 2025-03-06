# app/__init__.py (Complete Example)
from flask import Flask, request, g
from dotenv import load_dotenv
from app.config import Config, DevelopmentConfig, ProductionConfig
from app.extensions import db, migrate, babel  # Import babel
from app.routes import init_app as init_routes
from app.api import api_bp
import click
from app.utils.load_geojson import load_geojson
from app.models.energy_models import AlgeriaWelayes, AlgeriaBoundary
from datetime import datetime


def get_locale():
    # Get language from URL parameter, fallback to best match from Accept-Language header
    lang = request.args.get('lang')
    if lang in ['en', 'fr', 'ar']:
        return lang
    return request.accept_languages.best_match(['en', 'fr', 'ar'])


def create_app(config_class=DevelopmentConfig):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)        # Initialize SQLAlchemy
    migrate.init_app(app, db)  # Initialize Flask-Migrate
    
    # Configure Babel
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr', 'ar']
    babel.init_app(app, locale_selector=get_locale)

    @app.before_request
    def before_request():
        g.lang = get_locale()
        g.language_name = {'en': 'English', 'fr': 'Français', 'ar': 'العربية'}[g.lang]

    @app.context_processor
    def inject_year():
        return {'year': datetime.now().year}

    init_routes(app)
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.cli.command("load-geojson-data")
    @click.option('--geojson', is_flag=True, help='Load GeoJSON data.')
    def load_data(geojson):
        if geojson:
            with app.app_context():
                try:
                    load_geojson('app/utils/algeria_welayes.json', AlgeriaWelayes)
                    load_geojson('app/utils/algeria_boundry.json', AlgeriaBoundary)
                    print("GeoJSON data loaded successfully.")
                except Exception as e:
                    print(f"Error loading GeoJSON data: {e}")
        else:
            click.echo('Please specify --geojson')
    return app