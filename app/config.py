# app/config.py (Complete Example)
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key') #Use default value
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') #Get the variable from the environment
    CACHE_TYPE = 'simple'  # Use 'redis' in production
    CACHE_REDIS_URL = 'redis://localhost:6379/0'

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    # Production-specific settings (use environment variables)
    CACHE_TYPE = 'redis'
    # DATABASE_URL *must* be set in the environment