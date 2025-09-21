"""
Esquemas de Swagger para rutas de desarrolladoras.
"""

get_desarrolladoras_schema = {
    'tags': ['Desarrolladoras'],
    'summary': 'Obtener todas las desarrolladoras',
    'description': 'Obtiene una lista de todas las desarrolladoras con filtros opcionales',
    'parameters': [
        {
            'name': 'buscar',
            'in': 'query',
            'type': 'string',
            'description': 'Buscar en nombre, país y descripción',
            'example': 'nintendo'
        },
        {
            'name': 'pais',
            'in': 'query',
            'type': 'string',
            'description': 'Filtrar por país',
            'example': 'Japón'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de desarrolladoras obtenida exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Desarrolladoras obtenidas exitosamente'},
                    'data': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/Desarrolladora'}
                    },
                    'count': {'type': 'integer', 'example': 10},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        500: {'$ref': '#/responses/InternalServerError'}
    }
}

get_desarrolladora_schema = {
    'tags': ['Desarrolladoras'],
    'summary': 'Obtener una desarrolladora específica',
    'description': 'Obtiene una desarrolladora por su ID',
    'parameters': [
        {
            'name': 'desarrolladora_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la desarrolladora',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': 'Desarrolladora obtenida exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Desarrolladora obtenida exitosamente'},
                    'data': {'$ref': '#/definitions/Desarrolladora'},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        404: {'$ref': '#/responses/NotFound'},
        500: {'$ref': '#/responses/InternalServerError'}
    }
}

create_desarrolladora_schema = {
    'tags': ['Desarrolladoras'],
    'summary': 'Crear una nueva desarrolladora',
    'description': 'Crea una nueva desarrolladora en el sistema',
    'parameters': [
        {
            'name': 'desarrolladora',
            'in': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/DesarrolladoraInput'}
        }
    ],
    'responses': {
        201: {
            'description': 'Desarrolladora creada exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Desarrolladora creada exitosamente'},
                    'data': {'$ref': '#/definitions/Desarrolladora'},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {'$ref': '#/responses/BadRequest'},
        500: {'$ref': '#/responses/InternalServerError'}
    }
}

update_desarrolladora_schema = {
    'tags': ['Desarrolladoras'],
    'summary': 'Actualizar una desarrolladora',
    'description': 'Actualiza una desarrolladora existente',
    'parameters': [
        {
            'name': 'desarrolladora_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la desarrolladora',
            'example': 1
        },
        {
            'name': 'desarrolladora',
            'in': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/DesarrolladoraUpdateInput'}
        }
    ],
    'responses': {
        200: {
            'description': 'Desarrolladora actualizada exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Desarrolladora actualizada exitosamente'},
                    'data': {'$ref': '#/definitions/Desarrolladora'},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {'$ref': '#/responses/BadRequest'},
        404: {'$ref': '#/responses/NotFound'},
        500: {'$ref': '#/responses/InternalServerError'}
    }
}

delete_desarrolladora_schema = {
    'tags': ['Desarrolladoras'],
    'summary': 'Eliminar una desarrolladora',
    'description': 'Elimina una desarrolladora del sistema',
    'parameters': [
        {
            'name': 'desarrolladora_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la desarrolladora',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': 'Desarrolladora eliminada exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Desarrolladora eliminada exitosamente'},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {'$ref': '#/responses/BadRequest'},
        404: {'$ref': '#/responses/NotFound'},
        500: {'$ref': '#/responses/InternalServerError'}
    }
}

get_paises_schema = {
    'tags': ['Desarrolladoras'],
    'summary': 'Obtener países únicos',
    'description': 'Obtiene una lista de todos los países únicos de las desarrolladoras',
    'responses': {
        200: {
            'description': 'Países obtenidos exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Países obtenidos exitosamente'},
                    'data': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'example': ['Japón', 'Estados Unidos', 'Francia', 'Reino Unido']
                    },
                    'count': {'type': 'integer', 'example': 4},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        500: {'$ref': '#/responses/InternalServerError'}
    }
}

get_estadisticas_desarrolladoras_schema = {
    'tags': ['Desarrolladoras'],
    'summary': 'Obtener estadísticas generales',
    'description': 'Obtiene estadísticas generales de todas las desarrolladoras',
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
                            'total_desarrolladoras': {'type': 'integer', 'example': 25},
                            'paises_unicos': {'type': 'integer', 'example': 8},
                            'con_sitio_web': {'type': 'integer', 'example': 20},
                            'con_descripcion': {'type': 'integer', 'example': 18}
                        }
                    },
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        500: {'$ref': '#/responses/InternalServerError'}
    }
}

get_videojuegos_desarrolladora_schema = {
    'tags': ['Desarrolladoras'],
    'summary': 'Obtener videojuegos de una desarrolladora',
    'description': 'Obtiene todos los videojuegos desarrollados por una desarrolladora específica',
    'parameters': [
        {
            'name': 'desarrolladora_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la desarrolladora',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': 'Videojuegos de la desarrolladora obtenidos exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Videojuegos de la desarrolladora obtenidos exitosamente'},
                    'data': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/Videojuego'}
                    },
                    'count': {'type': 'integer', 'example': 5},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        404: {'$ref': '#/responses/NotFound'},
        500: {'$ref': '#/responses/InternalServerError'}
    }
}

get_estadisticas_desarrolladora_schema = {
    'tags': ['Desarrolladoras'],
    'summary': 'Obtener estadísticas de una desarrolladora',
    'description': 'Obtiene estadísticas específicas de una desarrolladora',
    'parameters': [
        {
            'name': 'desarrolladora_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la desarrolladora',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': 'Estadísticas de la desarrolladora obtenidas exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Estadísticas de la desarrolladora obtenidas exitosamente'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'desarrolladora': {'$ref': '#/definitions/Desarrolladora'},
                            'total_videojuegos': {'type': 'integer', 'example': 5},
                            'valoracion_promedio': {'type': 'number', 'format': 'float', 'example': 8.5},
                            'precio_promedio': {'type': 'number', 'format': 'float', 'example': 45.99},
                            'categorias_desarrolladas': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'example': ['RPG', 'Aventura', 'Acción']
                            }
                        }
                    },
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        404: {'$ref': '#/responses/NotFound'},
        500: {'$ref': '#/responses/InternalServerError'}
    }
}