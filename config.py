import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    BASE_DIR = Path(__file__).resolve().parent
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    ALLOWED_EXTENSIONS = {'pdf'}
    LOG_DIR = BASE_DIR / 'logs'
    # Ensuring log directory exists
    LOG_DIR.mkdir(exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = os.getenv('DEBUG', True) # Default to True if not set
    UPLOAD_FOLDER = Config.BASE_DIR / 'uploads' / 'development'
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

class ProductionConfig(Config):
    DEBUG = False
    UPLOAD_FOLDER = Config.BASE_DIR / 'uploads' / 'production'
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    UPLOAD_FOLDER = Config.BASE_DIR / 'uploads' / 'testing'
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
