"""
Aplicación principal de Flask para la API de Videojuegos.
"""
import os
from flask import Flask, redirect, url_for
from flasgger import Swagger
from dotenv import load_dotenv

# Importar módulos de la aplicación
from src.Config.Database import init_db, create_tables
from src.Routes import register_blueprints
from src.Schemas import get_swagger_config, get_swagger_template
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
    # Inicializar Swagger
    Swagger(app, config=get_swagger_config(), template=get_swagger_template())
    
    # Inicializar base de datos
    init_db(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Configurar middlewares
    register_error_handlers(app)
    setup_logging(app)
    log_request_info(app)
    setup_cors(app)
    
    # Configurar middlewares de seguridad
    from src.Middlewares.error_handler import setup_security_middlewares
    setup_security_middlewares(app)
    
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
