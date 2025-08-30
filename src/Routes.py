from flask import Blueprint
from flasgger import swag_from
from src.Controllers.VideojuegoController import VideojuegoController
from src.Utils import create_response

# Crear el blueprint para las rutas de videojuegos
videojuegos_bp = Blueprint('videojuegos', __name__)

# Rutas para operaciones CRUD de videojuegos

@videojuegos_bp.route('/videojuegos', methods=['GET'])
@swag_from({
    'tags': ['Videojuegos'],
    'summary': 'Obtener todos los videojuegos',
    'description': 'Obtiene una lista de todos los videojuegos disponibles con filtros opcionales',
    'parameters': [
        {
            'name': 'categoria',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filtrar videojuegos por categoría (ej: Aventura, Acción, RPG)',
            'example': 'Aventura'
        },
        {
            'name': 'buscar',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Buscar videojuegos por nombre o categoría',
            'example': 'Super'
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
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'nombre': {'type': 'string', 'example': 'The Legend of Zelda'},
                                'categoria': {'type': 'string', 'example': 'Aventura'},
                                'precio': {'type': 'number', 'example': 59.99},
                                'valoracion': {'type': 'number', 'example': 9.5},
                                'fecha_creacion': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'},
                                'fecha_actualizacion': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                            }
                        }
                    },
                    'timestamp': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                }
            }
        }
    }
})
def get_all_videojuegos():
    """Obtiene todos los videojuegos con filtros opcionales"""
    return VideojuegoController.get_all_videojuegos()

@videojuegos_bp.route('/videojuegos/<int:game_id>', methods=['GET'])
@swag_from({
    'tags': ['Videojuegos'],
    'summary': 'Obtener videojuego por ID',
    'description': 'Obtiene un videojuego específico utilizando su identificador único',
    'parameters': [
        {
            'name': 'game_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID único del videojuego',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': 'Videojuego encontrado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Videojuego encontrado'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'nombre': {'type': 'string', 'example': 'The Legend of Zelda'},
                            'categoria': {'type': 'string', 'example': 'Aventura'},
                            'precio': {'type': 'number', 'example': 59.99},
                            'valoracion': {'type': 'number', 'example': 9.5},
                            'fecha_creacion': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'},
                            'fecha_actualizacion': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                        }
                    },
                    'timestamp': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                }
            }
        },
        404: {
            'description': 'Videojuego no encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': 'Videojuego no encontrado'},
                    'data': {'type': 'null'},
                    'timestamp': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                }
            }
        }
    }
})
def get_videojuego_by_id(game_id):
    """Obtiene un videojuego específico por su ID"""
    return VideojuegoController.get_videojuego_by_id(game_id)

@videojuegos_bp.route('/videojuegos', methods=['POST'])
@swag_from({
    'tags': ['Videojuegos'],
    'summary': 'Crear nuevo videojuego',
    'description': 'Crea un nuevo videojuego con la información proporcionada',
    'parameters': [
        {
            'name': 'videojuego',
            'in': 'body',
            'required': True,
            'description': 'Datos del videojuego a crear',
            'schema': {
                'type': 'object',
                'required': ['nombre', 'categoria', 'precio', 'valoracion'],
                'properties': {
                    'nombre': {'type': 'string', 'example': 'Super Mario Odyssey', 'description': 'Nombre del videojuego'},
                    'categoria': {'type': 'string', 'example': 'Aventura', 'description': 'Categoría del videojuego'},
                    'precio': {'type': 'number', 'example': 49.99, 'description': 'Precio del videojuego'},
                    'valoracion': {'type': 'number', 'example': 9.2, 'minimum': 0, 'maximum': 10, 'description': 'Valoración del videojuego (0-10)'}
                }
            }
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
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 6},
                            'nombre': {'type': 'string', 'example': 'Super Mario Odyssey'},
                            'categoria': {'type': 'string', 'example': 'Aventura'},
                            'precio': {'type': 'number', 'example': 49.99},
                            'valoracion': {'type': 'number', 'example': 9.2},
                            'fecha_creacion': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'},
                            'fecha_actualizacion': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                        }
                    },
                    'timestamp': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                }
            }
        },
        400: {
            'description': 'Datos inválidos o faltantes',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': 'Datos faltantes o inválidos'},
                    'data': {'type': 'null'},
                    'timestamp': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                }
            }
        }
    }
})
def create_videojuego():
    """Crea un nuevo videojuego"""
    return VideojuegoController.create_videojuego()

@videojuegos_bp.route('/videojuegos/<int:game_id>', methods=['PUT'])
@swag_from({
    'tags': ['Videojuegos'],
    'summary': 'Actualizar videojuego',
    'description': 'Actualiza un videojuego existente con nueva información',
    'parameters': [
        {
            'name': 'game_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID único del videojuego a actualizar',
            'example': 1
        },
        {
            'name': 'videojuego',
            'in': 'body',
            'required': True,
            'description': 'Nuevos datos del videojuego',
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string', 'example': 'The Legend of Zelda: Breath of the Wild'},
                    'categoria': {'type': 'string', 'example': 'Aventura'},
                    'precio': {'type': 'number', 'example': 39.99},
                    'valoracion': {'type': 'number', 'example': 9.8, 'minimum': 0, 'maximum': 10}
                }
            }
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
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'nombre': {'type': 'string', 'example': 'The Legend of Zelda: Breath of the Wild'},
                            'categoria': {'type': 'string', 'example': 'Aventura'},
                            'precio': {'type': 'number', 'example': 39.99},
                            'valoracion': {'type': 'number', 'example': 9.8},
                            'fecha_creacion': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'},
                            'fecha_actualizacion': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                        }
                    },
                    'timestamp': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                }
            }
        },
        404: {
            'description': 'Videojuego no encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': 'Videojuego no encontrado'},
                    'data': {'type': 'null'},
                    'timestamp': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                }
            }
        }
    }
})
def update_videojuego(game_id):
    """Actualiza un videojuego existente"""
    return VideojuegoController.update_videojuego(game_id)

@videojuegos_bp.route('/videojuegos/<int:game_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Videojuegos'],
    'summary': 'Eliminar videojuego',
    'description': 'Elimina un videojuego específico del sistema',
    'parameters': [
        {
            'name': 'game_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID único del videojuego a eliminar',
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
                    'data': {'type': 'null'},
                    'timestamp': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                }
            }
        },
        404: {
            'description': 'Videojuego no encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': 'Videojuego no encontrado'},
                    'data': {'type': 'null'},
                    'timestamp': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                }
            }
        }
    }
})
def delete_videojuego(game_id):
    """Elimina un videojuego"""
    return VideojuegoController.delete_videojuego(game_id)

# Ruta adicional para obtener información de la API
@videojuegos_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['API Info'],
    'summary': 'Información de la API',
    'description': 'Obtiene información básica sobre la API de videojuegos',
    'responses': {
        200: {
            'description': 'Información de la API obtenida exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'API funcionando correctamente'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'nombre': {'type': 'string', 'example': 'API de Videojuegos'},
                            'version': {'type': 'string', 'example': '1.0.0'},
                            'descripcion': {'type': 'string'},
                            'endpoints': {'type': 'object'}
                        }
                    },
                    'timestamp': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                }
            }
        }
    }
})
def api_info():
    """Información básica de la API"""
    info = {
        'nombre': '🎮 API de Videojuegos',
        'version': '1.0.0',
        'descripcion': 'API REST para gestionar videojuegos con operaciones CRUD',
        'autor': 'Miguel Bonilla',
        'documentacion_swagger': '/apidocs/',
        'endpoints': {
            'GET /api/': 'Información de la API',
            'GET /api/videojuegos': 'Obtener todos los videojuegos',
            'GET /api/videojuegos?categoria=<categoria>': 'Filtrar por categoría',
            'GET /api/videojuegos?buscar=<termino>': 'Buscar videojuegos',
            'GET /api/videojuegos/<id>': 'Obtener videojuego por ID',
            'POST /api/videojuegos': 'Crear nuevo videojuego',
            'PUT /api/videojuegos/<id>': 'Actualizar videojuego',
            'DELETE /api/videojuegos/<id>': 'Eliminar videojuego'
        },
        'filtros_disponibles': [
            'categoria - Filtrar por categoría',
            'buscar - Buscar en nombre y categoría'
        ],
        'categorias_ejemplo': [
            'Aventura', 'Acción', 'RPG', 'Deportes', 
            'Sandbox', 'Multijugador', 'Estrategia'
        ]
    }
    
    return create_response(
        success=True,
        message="API de Videojuegos funcionando correctamente 🚀",
        data=info,
        status_code=200
    )