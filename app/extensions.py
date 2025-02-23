# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_caching import Cache

db = SQLAlchemy()
babel = Babel()
cache = Cache()

def init_app(app):
    db.init_app(app)
    babel.init_app(app)
    cache.init_app(app)