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
    busqueda_avanzada_schema,
    importar_externa_schema,
    importar_batch_schema,
    get_enriquecido_schema,
    buscar_hibrida_schema,
    sync_manual_schema,
    sync_status_schema
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

# DEPRECATED: Usar /importar-batch en su lugar
# @videojuegos_bp.route('/importar-externa', methods=['POST'])
# @swag_from(importar_externa_schema)
# def importar_externa():
#     """Endpoint para importar un videojuego desde RAWG API."""
#     return VideojuegoController.importar_externa()

@videojuegos_bp.route('/importar-batch', methods=['POST'])
@swag_from(importar_batch_schema)
def importar_batch():
    """
    Endpoint para importar videojuegos desde RAWG API.
    Si no se proporcionan juegos, importa automáticamente 5-6 juegos populares.
    """
    return VideojuegoController.importar_batch()

@videojuegos_bp.route('/<int:videojuego_id>/enriquecido', methods=['GET'])
@swag_from(get_enriquecido_schema)
def get_enriquecido(videojuego_id):
    """Endpoint para obtener un videojuego con datos enriquecidos de RAWG."""
    return VideojuegoController.get_enriquecido(videojuego_id)

@videojuegos_bp.route('/buscar', methods=['GET'])
@swag_from(buscar_hibrida_schema)
def buscar_hibrida():
    """Endpoint para búsqueda híbrida (local + RAWG)."""
    return VideojuegoController.buscar_hibrida()

# DEPRECATED: Usar /importar-batch en su lugar (importa juegos populares automáticamente)
# @videojuegos_bp.route('/sync-manual', methods=['POST'])
# @swag_from(sync_manual_schema)
# def sync_manual():
#     """Endpoint para iniciar sincronización asíncrona manual."""
#     return VideojuegoController.sync_manual()

@videojuegos_bp.route('/sync-status/<task_id>', methods=['GET'])
@swag_from(sync_status_schema)
def sync_status(task_id):
    """Endpoint para consultar estado de sincronización."""
    return VideojuegoController.sync_status(task_id)
