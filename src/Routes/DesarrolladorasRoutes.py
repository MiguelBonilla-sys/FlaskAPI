"""
Rutas específicas para la gestión de desarrolladoras.
"""
from flask import Blueprint
from flasgger import swag_from
from src.Controllers.DesarrolladoraController import DesarrolladoraController
from src.Schemas.DesarrolladorasSchema import (
    get_desarrolladoras_schema,
    get_desarrolladora_schema,
    create_desarrolladora_schema,
    update_desarrolladora_schema,
    delete_desarrolladora_schema,
    get_paises_schema,
    get_estadisticas_desarrolladoras_schema,
    get_videojuegos_desarrolladora_schema,
    get_estadisticas_desarrolladora_schema
)

# Crear blueprint para las rutas de desarrolladoras
desarrolladoras_bp = Blueprint('desarrolladoras', __name__, url_prefix='/api/desarrolladoras')

@desarrolladoras_bp.route('', methods=['GET'])
@swag_from(get_desarrolladoras_schema)
def get_desarrolladoras():
    """Endpoint para obtener todas las desarrolladoras con filtros opcionales."""
    return DesarrolladoraController.get_all()

@desarrolladoras_bp.route('/<int:desarrolladora_id>', methods=['GET'])
@swag_from(get_desarrolladora_schema)
def get_desarrolladora(desarrolladora_id):
    """Endpoint para obtener una desarrolladora específica por ID."""
    return DesarrolladoraController.get_by_id(desarrolladora_id)

@desarrolladoras_bp.route('', methods=['POST'])
@swag_from(create_desarrolladora_schema)
def create_desarrolladora():
    """Endpoint para crear una nueva desarrolladora."""
    return DesarrolladoraController.create()

@desarrolladoras_bp.route('/<int:desarrolladora_id>', methods=['PUT'])
@swag_from(update_desarrolladora_schema)
def update_desarrolladora(desarrolladora_id):
    """Endpoint para actualizar una desarrolladora existente."""
    return DesarrolladoraController.update(desarrolladora_id)

@desarrolladoras_bp.route('/<int:desarrolladora_id>', methods=['DELETE'])
@swag_from(delete_desarrolladora_schema)
def delete_desarrolladora(desarrolladora_id):
    """Endpoint para eliminar una desarrolladora."""
    return DesarrolladoraController.delete(desarrolladora_id)

@desarrolladoras_bp.route('/paises', methods=['GET'])
@swag_from(get_paises_schema)
def get_paises():
    """Endpoint para obtener todos los países únicos de desarrolladoras."""
    return DesarrolladoraController.get_paises()

@desarrolladoras_bp.route('/estadisticas', methods=['GET'])
@swag_from(get_estadisticas_desarrolladoras_schema)
def get_estadisticas():
    """Endpoint para obtener estadísticas generales de desarrolladoras."""
    return DesarrolladoraController.get_statistics()

@desarrolladoras_bp.route('/<int:desarrolladora_id>/videojuegos', methods=['GET'])
@swag_from(get_videojuegos_desarrolladora_schema)
def get_videojuegos_desarrolladora(desarrolladora_id):
    """Endpoint para obtener todos los videojuegos de una desarrolladora específica."""
    return DesarrolladoraController.get_videojuegos(desarrolladora_id)

@desarrolladoras_bp.route('/<int:desarrolladora_id>/estadisticas', methods=['GET'])
@swag_from(get_estadisticas_desarrolladora_schema)
def get_estadisticas_desarrolladora(desarrolladora_id):
    """Endpoint para obtener estadísticas específicas de una desarrolladora."""
    return DesarrolladoraController.get_estadisticas_desarrolladora(desarrolladora_id)