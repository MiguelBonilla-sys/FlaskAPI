from flask import Flask
from flasgger import Swagger
from src.Routes import videojuegos_bp
from src.Config import config
from src.Middlewares import register_middlewares
import os

def create_app(config_name=None):
    """Factory function para crear la aplicación Flask con Swagger"""
    
    # Determinar el tipo de configuración
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config.get(config_name, config['default']))
    
    # Configuración de Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "🎮 API de Videojuegos",
            "description": "API REST completa para gestionar videojuegos con operaciones CRUD. Esta API permite crear, leer, actualizar y eliminar videojuegos, así como buscar y filtrar por categorías.",
            "contact": {
                "name": "Miguel Bonilla",
                "email": "miguel@example.com"
            },
            "version": "1.0.0"
        },
        "host": "localhost:5000",
        "basePath": "/api",
        "schemes": [
            "http"
        ],
        "consumes": [
            "application/json"
        ],
        "produces": [
            "application/json"
        ],
        "tags": [
            {
                "name": "Videojuegos",
                "description": "Operaciones CRUD para videojuegos"
            },
            {
                "name": "API Info",
                "description": "Información general de la API"
            }
        ]
    }
    
    # Inicializar Swagger
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Registrar middlewares
    register_middlewares(app)
    
    # Registrar blueprints
    app.register_blueprint(videojuegos_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("🎮 Iniciando API de Videojuegos con Swagger...")
    print("🌐 Servidor corriendo en: http://localhost:5000")
    print("📚 Documentación Swagger: http://localhost:5000/apidocs/")
    print("ℹ️  Información de la API: http://localhost:5000/api/")
    print(f"🔧 Modo debug: {app.debug}")
    print("\n✨ ¡API lista para usar! Visita la documentación Swagger para probar los endpoints.")
    
    app.run(debug=True, host='0.0.0.0', port=5000)