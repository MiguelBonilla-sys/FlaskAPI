"""
Aplicación principal de Flask para la API de Videojuegos.
"""
import os
from flask import Flask, redirect, url_for
from flasgger import Swagger
from dotenv import load_dotenv

# Importar módulos de la aplicación
from src.Config.Database import init_db, create_tables
from src.Routes import api_bp, general_bp, get_swagger_definitions, get_swagger_responses
from src.Middlewares.error_handler import register_error_handlers, setup_logging, log_request_info, setup_cors

# Cargar variables de entorno
load_dotenv()

def create_app():
    """
    Factory function para crear la aplicación Flask.
    
    Returns:
        Flask: Instancia configurada de la aplicación
    """
    app = Flask(__name__)
    
    # Configuraciones de la aplicación
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Configurar Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": os.getenv('API_TITLE', 'Videojuegos API'),
            "description": os.getenv('API_DESCRIPTION', 'API REST para gestión de videojuegos'),
            "version": os.getenv('API_VERSION', 'v1'),
            "contact": {
                "name": "API Support",
                "email": "support@videojuegosapi.com"
            },
            "license": {
                "name": "MIT License",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "definitions": get_swagger_definitions(),
        "responses": get_swagger_responses(),
        "tags": [
            {
                "name": "Sistema",
                "description": "Endpoints del sistema y health checks"
            },
            {
                "name": "API Info",
                "description": "Información general de la API"
            },
            {
                "name": "Videojuegos",
                "description": "Operaciones CRUD para videojuegos"
            }
        ]
    }
    
    # Inicializar Swagger
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Inicializar base de datos
    init_db(app)
    
    # Registrar blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(general_bp)
    
    # Configurar middlewares
    register_error_handlers(app)
    setup_logging(app)
    log_request_info(app)
    setup_cors(app)
    
    # Ruta raíz que redirige a la documentación
    @app.route('/')
    def index():
        """Redirige a la documentación de Swagger."""
        return redirect(url_for('flasgger.apidocs'))
    
    return app

def init_database():
    """
    Inicializa la base de datos creando las tablas necesarias.
    """
    with app.app_context():
        try:
            create_tables()
            print("✅ Tablas de la base de datos creadas exitosamente")
        except Exception as e:
            print(f"❌ Error al crear las tablas: {str(e)}")

if __name__ == '__main__':
    # Crear la aplicación
    app = create_app()
    
    # Inicializar base de datos
    init_database()
    
    # Configurar host y puerto
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"""
🚀 Iniciando API de Videojuegos
📍 Servidor: http://{host}:{port}
📚 Documentación: http://{host}:{port}/apidocs/
🔗 API Base: http://{host}:{port}/api/
💚 Salud: http://{host}:{port}/health
    """)
    
    # Ejecutar la aplicación
    app.run(
        host=host,
        port=port,
        debug=debug
    )
