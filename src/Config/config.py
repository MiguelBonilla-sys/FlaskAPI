import os
from datetime import timedelta

class Config:
    """Configuración base de la aplicación"""
    
    # Configuración básica de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Configuración de JSON
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Configuración de CORS (si se necesita en el futuro)
    CORS_ENABLED = os.environ.get('CORS_ENABLED', 'True').lower() == 'true'
    
    # Configuración de la API
    API_VERSION = '1.0.0'
    API_TITLE = 'API de Videojuegos'
    API_DESCRIPTION = 'API REST para gestionar videojuegos con operaciones CRUD'

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Configuración para testing"""
    DEBUG = True
    TESTING = True

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
