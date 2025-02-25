# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Migrate
from flask_babel import Babel
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()  # Create Migrate instance
babel = Babel()
cache = Cache()

def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Migrate with app and db
    babel.init_app(app)
    cache.init_app(app)