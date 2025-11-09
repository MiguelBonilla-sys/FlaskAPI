"""
Configuración compartida para pytest.
"""
import os
import sys
import pytest

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope='session')
def app():
    """Fixture para la aplicación Flask."""
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Configurar variables de entorno de prueba
    os.environ['RAWG_API_KEY'] = 'test_key'
    os.environ['REDIS_URL'] = 'redis://localhost:6379/1'  # DB diferente para tests
    
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def client(app):
    """Fixture para el cliente de pruebas."""
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    """Fixture para sesión de base de datos con rollback automático."""
    from src.Config.Database import db
    
    # Crear todas las tablas
    db.create_all()
    
    yield db.session
    
    # Limpiar después del test
    db.session.rollback()
    db.drop_all()


@pytest.fixture
def sample_rawg_data():
    """Fixture con datos de ejemplo de RAWG API."""
    return {
        'id': 3328,
        'name': 'The Witcher 3: Wild Hunt',
        'genres': [{'name': 'RPG'}, {'name': 'Action'}],
        'rating': 4.5,
        'metacritic': 92,
        'description_raw': 'A great RPG game with amazing story.',
        'background_image': 'https://example.com/witcher3.jpg',
        'developers': [{'name': 'CD Projekt RED'}],
        'platforms': [
            {'platform': {'name': 'PC'}},
            {'platform': {'name': 'PlayStation 4'}}
        ],
        'tags': [
            {'name': 'Open World'},
            {'name': 'Fantasy'}
        ]
    }

