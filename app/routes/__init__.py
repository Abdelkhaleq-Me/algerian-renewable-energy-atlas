# app/routes/__init__.py
from flask import Flask
from .home import home_bp
from .atlas import atlas_bp
from .download import download_bp
from .about import about_bp
from .contact import contact_bp

def init_app(app: Flask):
    app.register_blueprint(home_bp)
    app.register_blueprint(atlas_bp)
    app.register_blueprint(download_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(contact_bp)