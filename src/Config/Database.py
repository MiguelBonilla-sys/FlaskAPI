"""
Configuración de la base de datos PostgreSQL.
"""
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear instancias de SQLAlchemy y Migrate
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """
    Inicializa la configuración de la base de datos con la aplicación Flask.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    # Verificar si hay una URL de base de datos personalizada
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Usar URL personalizada (por ejemplo, SQLite para desarrollo)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Configuración de PostgreSQL usando variables de entorno
        postgres_user = os.getenv('PGUSER', 'postgres')
        postgres_password = os.getenv('PGPASSWORD', '')
        postgres_host = os.getenv('PGHOST', 'localhost')
        postgres_port = os.getenv('PGPORT', '5432')
        postgres_db = os.getenv('PGDATABASE', 'videojuegos_db')
        
        # URI de conexión PostgreSQL
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f'postgresql://{postgres_user}:{postgres_password}@'
            f'{postgres_host}:{postgres_port}/{postgres_db}'
        )
    
    # Configuraciones adicionales de SQLAlchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    
    return db

def create_tables():
    """
    Crea todas las tablas definidas en los modelos.
    """
    db.create_all()

def get_db():
    """
    Obtiene la instancia de la base de datos.
    
    Returns:
        SQLAlchemy: Instancia de la base de datos
    """
    return db
