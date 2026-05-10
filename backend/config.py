# Configuration for Flight Scheduler Backend
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / 'instance'
INSTANCE_DIR.mkdir(exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'aircraft-network-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ALLOW_ORIGINS = ['*']

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{INSTANCE_DIR / "flights.db"}')
