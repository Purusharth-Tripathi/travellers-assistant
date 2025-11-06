"""
Configuration file for Traveller's Assistant App
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    PORT = int(os.getenv('PORT', 5000))
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    EXCHANGE_RATE_API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
    GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY')
    
    # API Endpoints
    OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'
    REST_COUNTRIES_BASE_URL = 'https://restcountries.com/v3.1'
    EXCHANGE_RATE_BASE_URL = 'https://v6.exchangerate-api.com/v6'
    
    # App Settings
    MAX_TRAVELERS = 20
    MAX_DAYS = 365
    CACHE_TIMEOUT = 3600  # 1 hour
    
    @staticmethod
    def validate_config():
        """Validate that essential configuration is present"""
        missing = []

        if not Config.GEMINI_API_KEY:
            missing.append('GEMINI_API_KEY')
        if not Config.OPENWEATHER_API_KEY:
            missing.append('OPENWEATHER_API_KEY')

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return True
