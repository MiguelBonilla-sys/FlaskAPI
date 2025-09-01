"""
Definición de rutas de la API con documentación Swagger.
"""
from flask import Blueprint
from flasgger import swag_from
from src.Controllers.VideojuegoController import VideojuegoController
from src.Utils import get_api_info, create_response
import os

# Crear blueprint para las rutas de la API
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Crear blueprint para rutas generales (sin prefijo)
general_bp = Blueprint('general', __name__)

@general_bp.route('/health', methods=['GET'])
@swag_from({
    'tags': ['Sistema'],
    'summary': 'Health Check',
    'description': 'Verifica el estado de salud de la API',
    'responses': {
        200: {
            'description': 'API funcionando correctamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'healthy'},
                    'message': {'type': 'string', 'example': 'API funcionando correctamente'},
                    'version': {'type': 'string', 'example': 'v1'}
                }
            }
        }
    }
})
def health():
    """Endpoint de verificación de salud de la aplicación."""
    return {
        'status': 'healthy',
        'message': 'API funcionando correctamente',
        'version': os.getenv('API_VERSION', 'v1')
    }

@api_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['API Info'],
    'summary': 'Información de la API',
    'description': 'Obtiene información básica de la API y lista de endpoints disponibles',
    'responses': {
        200: {
            'description': 'Información de la API obtenida exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Información de la API obtenida exitosamente'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string', 'example': 'Videojuegos API'},
                            'version': {'type': 'string', 'example': 'v1'},
                            'description': {'type': 'string', 'example': 'API REST para gestión de videojuegos'},
                            'endpoints': {'type': 'object'}
                        }
                    },
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        }
    }
})
def get_api_info_route():
    """Endpoint para obtener información de la API."""
    return create_response(
        success=True,
        message="Información de la API obtenida exitosamente",
        data=get_api_info()
    )

@api_bp.route('/videojuegos', methods=['GET'])
@swag_from({
    'tags': ['Videojuegos'],
    'summary': 'Obtener todos los videojuegos',
    'description': 'Obtiene una lista de todos los videojuegos con filtros opcionales',
    'parameters': [
        {
            'name': 'categoria',
            'in': 'query',
            'type': 'string',
            'description': 'Filtrar por categoría',
            'example': 'RPG'
        },
        {
            'name': 'buscar',
            'in': 'query',
            'type': 'string',
            'description': 'Buscar en nombre y categoría',
            'example': 'zelda'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de videojuegos obtenida exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Videojuegos obtenidos exitosamente'},
                    'data': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/Videojuego'}
                    },
                    'count': {'type': 'integer', 'example': 5},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        500: {'$ref': '#/responses/InternalServerError'}
    }
})
def get_videojuegos():
    """Endpoint para obtener todos los videojuegos."""
    return VideojuegoController.get_all()

@api_bp.route('/videojuegos/<int:videojuego_id>', methods=['GET'])
@swag_from({
    'tags': ['Videojuegos'],
    'summary': 'Obtener un videojuego específico',
    'description': 'Obtiene un videojuego por su ID',
    'parameters': [
        {
            'name': 'videojuego_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del videojuego',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': 'Videojuego obtenido exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Videojuego obtenido exitosamente'},
                    'data': {'$ref': '#/definitions/Videojuego'},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        404: {'$ref': '#/responses/NotFound'},
        500: {'$ref': '#/responses/InternalServerError'}
    }
})
def get_videojuego(videojuego_id):
    """Endpoint para obtener un videojuego específico."""
    return VideojuegoController.get_by_id(videojuego_id)

@api_bp.route('/videojuegos', methods=['POST'])
@swag_from({
    'tags': ['Videojuegos'],
    'summary': 'Crear un nuevo videojuego',
    'description': 'Crea un nuevo videojuego con los datos proporcionados',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/VideojuegoInput'}
        }
    ],
    'responses': {
        201: {
            'description': 'Videojuego creado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Videojuego creado exitosamente'},
                    'data': {'$ref': '#/definitions/Videojuego'},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {'$ref': '#/responses/BadRequest'},
        500: {'$ref': '#/responses/InternalServerError'}
    }
})
def create_videojuego():
    """Endpoint para crear un nuevo videojuego."""
    return VideojuegoController.create()

@api_bp.route('/videojuegos/<int:videojuego_id>', methods=['PUT'])
@swag_from({
    'tags': ['Videojuegos'],
    'summary': 'Actualizar un videojuego',
    'description': 'Actualiza los datos de un videojuego existente',
    'parameters': [
        {
            'name': 'videojuego_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del videojuego',
            'example': 1
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/VideojuegoUpdateInput'}
        }
    ],
    'responses': {
        200: {
            'description': 'Videojuego actualizado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Videojuego actualizado exitosamente'},
                    'data': {'$ref': '#/definitions/Videojuego'},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {'$ref': '#/responses/BadRequest'},
        404: {'$ref': '#/responses/NotFound'},
        500: {'$ref': '#/responses/InternalServerError'}
    }
})
def update_videojuego(videojuego_id):
    """Endpoint para actualizar un videojuego."""
    return VideojuegoController.update(videojuego_id)

@api_bp.route('/videojuegos/<int:videojuego_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Videojuegos'],
    'summary': 'Eliminar un videojuego',
    'description': 'Elimina un videojuego por su ID',
    'parameters': [
        {
            'name': 'videojuego_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del videojuego',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': 'Videojuego eliminado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Videojuego eliminado exitosamente'},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        404: {'$ref': '#/responses/NotFound'},
        500: {'$ref': '#/responses/InternalServerError'}
    }
})
def delete_videojuego(videojuego_id):
    """Endpoint para eliminar un videojuego."""
    return VideojuegoController.delete(videojuego_id)

@api_bp.route('/videojuegos/categorias', methods=['GET'])
@swag_from({
    'tags': ['Videojuegos'],
    'summary': 'Obtener categorías',
    'description': 'Obtiene todas las categorías únicas de videojuegos',
    'responses': {
        200: {
            'description': 'Categorías obtenidas exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Categorías obtenidas exitosamente'},
                    'data': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'example': ['RPG', 'Acción', 'Aventura', 'Deportes']
                    },
                    'count': {'type': 'integer', 'example': 4},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        500: {'$ref': '#/responses/InternalServerError'}
    }
})
def get_categorias():
    """Endpoint para obtener todas las categorías."""
    return VideojuegoController.get_categories()

@api_bp.route('/videojuegos/estadisticas', methods=['GET'])
@swag_from({
    'tags': ['Videojuegos'],
    'summary': 'Obtener estadísticas',
    'description': 'Obtiene estadísticas básicas de los videojuegos',
    'responses': {
        200: {
            'description': 'Estadísticas obtenidas exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Estadísticas obtenidas exitosamente'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'total_videojuegos': {'type': 'integer', 'example': 15},
                            'categorias_unicas': {'type': 'integer', 'example': 5},
                            'precio_promedio': {'type': 'number', 'example': 45.99},
                            'valoracion_promedio': {'type': 'number', 'example': 8.2}
                        }
                    },
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        500: {'$ref': '#/responses/InternalServerError'}
    }
})
def get_estadisticas():
    """Endpoint para obtener estadísticas."""
    return VideojuegoController.get_statistics()

# Definiciones de esquemas para Swagger
def get_swagger_definitions():
    """
    Retorna las definiciones de esquemas para Swagger.
    
    Returns:
        dict: Definiciones de esquemas
    """
    return {
        'Videojuego': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer', 'example': 1},
                'nombre': {'type': 'string', 'example': 'The Legend of Zelda: Breath of the Wild'},
                'categoria': {'type': 'string', 'example': 'Aventura'},
                'precio': {'type': 'number', 'format': 'float', 'example': 59.99},
                'valoracion': {'type': 'number', 'format': 'float', 'example': 9.7},
                'fecha_creacion': {'type': 'string', 'format': 'date-time'},
                'fecha_actualizacion': {'type': 'string', 'format': 'date-time'}
            }
        },
        'VideojuegoInput': {
            'type': 'object',
            'required': ['nombre', 'categoria', 'precio', 'valoracion'],
            'properties': {
                'nombre': {'type': 'string', 'example': 'The Witcher 3: Wild Hunt'},
                'categoria': {'type': 'string', 'example': 'RPG'},
                'precio': {'type': 'number', 'format': 'float', 'minimum': 0, 'example': 39.99},
                'valoracion': {'type': 'number', 'format': 'float', 'minimum': 0, 'maximum': 10, 'example': 9.3}
            }
        },
        'VideojuegoUpdateInput': {
            'type': 'object',
            'properties': {
                'nombre': {'type': 'string', 'example': 'The Witcher 3: Wild Hunt - Complete Edition'},
                'categoria': {'type': 'string', 'example': 'RPG'},
                'precio': {'type': 'number', 'format': 'float', 'minimum': 0, 'example': 29.99},
                'valoracion': {'type': 'number', 'format': 'float', 'minimum': 0, 'maximum': 10, 'example': 9.5}
            }
        }
    }

def get_swagger_responses():
    """
    Retorna las respuestas comunes para Swagger.
    
    Returns:
        dict: Definiciones de respuestas
    """
    return {
        'BadRequest': {
            'description': 'Petición incorrecta',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': 'Error en la validación de datos'},
                    'errors': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'example': ['El nombre es requerido']
                    },
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        'NotFound': {
            'description': 'Recurso no encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': 'Videojuego no encontrado'},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        'InternalServerError': {
            'description': 'Error interno del servidor',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': 'Error interno del servidor'},
                    'errors': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'example': ['Ha ocurrido un error inesperado en el servidor']
                    },
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        }
    }

# Función para obtener todos los blueprints
def get_blueprints():
    """
    Retorna todos los blueprints de la aplicación.
    
    Returns:
        list: Lista de blueprints
    """
    return [api_bp, general_bp]
