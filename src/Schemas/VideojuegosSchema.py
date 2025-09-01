"""
Esquemas de Swagger para rutas de videojuegos.
"""

get_videojuegos_schema = {
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
}

get_videojuego_schema = {
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
}

create_videojuego_schema = {
    'tags': ['Videojuegos'],
    'summary': 'Crear un nuevo videojuego',
    'description': 'Crea un nuevo videojuego con los datos proporcionados',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'Datos del videojuego a crear',
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
}

update_videojuego_schema = {
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
            'description': 'Datos del videojuego a actualizar',
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
}

delete_videojuego_schema = {
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
}

get_categorias_schema = {
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
}

get_estadisticas_schema = {
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
}
