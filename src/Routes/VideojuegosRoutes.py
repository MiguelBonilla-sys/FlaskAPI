"""
Rutas específicas para la gestión de videojuegos.
"""
from flask import Blueprint
from flasgger import swag_from
from src.Controllers.VideojuegoController import VideojuegoController
from src.Schemas.VideojuegosSchema import (
    get_videojuegos_schema,
    get_videojuego_schema,
    create_videojuego_schema,
    update_videojuego_schema,
    delete_videojuego_schema,
    get_categorias_schema,
    get_estadisticas_schema,
    busqueda_avanzada_schema
)

# Crear blueprint para las rutas de videojuegos
videojuegos_bp = Blueprint('videojuegos', __name__, url_prefix='/api/videojuegos')

@videojuegos_bp.route('', methods=['GET'])
@swag_from(get_videojuegos_schema)
def get_videojuegos():
    """Endpoint para obtener todos los videojuegos con filtros opcionales."""
    return VideojuegoController.get_all()

@videojuegos_bp.route('/<int:videojuego_id>', methods=['GET'])
@swag_from(get_videojuego_schema)
def get_videojuego(videojuego_id):
    """Endpoint para obtener un videojuego específico por ID."""
    return VideojuegoController.get_by_id(videojuego_id)

@videojuegos_bp.route('', methods=['POST'])
@swag_from(create_videojuego_schema)
def create_videojuego():
    """Endpoint para crear un nuevo videojuego."""
    return VideojuegoController.create()

@videojuegos_bp.route('/<int:videojuego_id>', methods=['PUT'])
@swag_from(update_videojuego_schema)
def update_videojuego(videojuego_id):
    """Endpoint para actualizar un videojuego existente."""
    return VideojuegoController.update(videojuego_id)

@videojuegos_bp.route('/<int:videojuego_id>', methods=['DELETE'])
@swag_from(delete_videojuego_schema)
def delete_videojuego(videojuego_id):
    """Endpoint para eliminar un videojuego."""
    return VideojuegoController.delete(videojuego_id)

@videojuegos_bp.route('/categorias', methods=['GET'])
@swag_from(get_categorias_schema)
def get_categorias():
    """Endpoint para obtener todas las categorías únicas."""
    return VideojuegoController.get_categories()

@videojuegos_bp.route('/estadisticas', methods=['GET'])
@swag_from(get_estadisticas_schema)
def get_estadisticas():
    """Endpoint para obtener estadísticas de videojuegos."""
    return VideojuegoController.get_statistics()

@videojuegos_bp.route('/busqueda-avanzada', methods=['GET'])
@swag_from(busqueda_avanzada_schema)
def busqueda_avanzada():
    """Endpoint para búsqueda avanzada con múltiples filtros."""
    return VideojuegoController.busqueda_avanzada()
