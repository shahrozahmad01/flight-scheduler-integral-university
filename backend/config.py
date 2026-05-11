# backend/config.py
# Aircraft Network Flight Scheduler
# Author: Mustafa Siddiqui | Roll: 2400100150 | MCA Integral University
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-mca-integral-2025')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///flight_scheduler.db'
    )

class ProductionConfig(Config):
    DEBUG = False
    _db_url = os.environ.get('DATABASE_URL')
    # Fix: Supabase gives 'postgres://' but SQLAlchemy needs 'postgresql://'
    if _db_url:
        if _db_url.startswith('postgres://'):
            _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = _db_url
    else:
        # Fallback to a local SQLite DB in case DATABASE_URL is not provided
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///flight_scheduler.db')

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

def get_config():
    env = os.environ.get('FLASK_ENV', 'development').lower()
    return config_map.get(env, DevelopmentConfig)