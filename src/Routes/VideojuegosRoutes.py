"""
Rutas específicas para la gestión de videojuegos.
"""
from flask import Blueprint
from flasgger import swag_from
from src.Controllers.VideojuegoController import VideojuegoController
from src.Middlewares.rate_limiter import rate_limit, strict_rate_limit
from src.Middlewares.auth import require_api_key, optional_api_key
from src.Middlewares.input_validation import validate_videojuego_data, validate_json_input
from src.Schemas.VideojuegosSchema import (
    get_videojuegos_schema,
    get_videojuego_schema,
    create_videojuego_schema,
    update_videojuego_schema,
    delete_videojuego_schema,
    get_categorias_schema,
    get_estadisticas_schema
)

# Crear blueprint para las rutas de videojuegos
videojuegos_bp = Blueprint('videojuegos', __name__, url_prefix='/api/videojuegos')

@videojuegos_bp.route('', methods=['GET'])
@swag_from(get_videojuegos_schema)
@rate_limit('requests_per_minute')
@optional_api_key()
def get_videojuegos():
    """Endpoint para obtener todos los videojuegos con filtros opcionales."""
    return VideojuegoController.get_all()

@videojuegos_bp.route('/<int:videojuego_id>', methods=['GET'])
@swag_from(get_videojuego_schema)
@rate_limit('requests_per_minute')
@optional_api_key()
def get_videojuego(videojuego_id):
    """Endpoint para obtener un videojuego específico por ID."""
    return VideojuegoController.get_by_id(videojuego_id)

@videojuegos_bp.route('', methods=['POST'])
@swag_from(create_videojuego_schema)
@validate_videojuego_data
@validate_json_input(sanitize=True)
@strict_rate_limit(10)  # Máximo 10 creaciones por minuto
@require_api_key('write')
def create_videojuego():
    """Endpoint para crear un nuevo videojuego."""
    return VideojuegoController.create()

@videojuegos_bp.route('/<int:videojuego_id>', methods=['PUT'])
@swag_from(update_videojuego_schema)
@validate_videojuego_data
@validate_json_input(sanitize=True)
@strict_rate_limit(15)  # Máximo 15 actualizaciones por minuto
@require_api_key('write')
def update_videojuego(videojuego_id):
    """Endpoint para actualizar un videojuego existente."""
    return VideojuegoController.update(videojuego_id)

@videojuegos_bp.route('/<int:videojuego_id>', methods=['DELETE'])
@swag_from(delete_videojuego_schema)
@strict_rate_limit(5)  # Máximo 5 eliminaciones por minuto
@require_api_key('delete')
def delete_videojuego(videojuego_id):
    """Endpoint para eliminar un videojuego."""
    return VideojuegoController.delete(videojuego_id)

@videojuegos_bp.route('/categorias', methods=['GET'])
@swag_from(get_categorias_schema)
@rate_limit('requests_per_minute')
@optional_api_key()
def get_categorias():
    """Endpoint para obtener todas las categorías únicas."""
    return VideojuegoController.get_categories()

@videojuegos_bp.route('/estadisticas', methods=['GET'])
@swag_from(get_estadisticas_schema)
@rate_limit('requests_per_hour')  # Limitado por hora por ser costoso
@optional_api_key()
def get_estadisticas():
    """Endpoint para obtener estadísticas de videojuegos."""
    return VideojuegoController.get_statistics()
