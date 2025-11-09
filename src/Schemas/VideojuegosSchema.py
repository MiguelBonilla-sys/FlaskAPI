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
            'description': 'Buscar en nombre, categoría y desarrolladora',
            'example': 'zelda'
        },
        {
            'name': 'desarrolladora_id',
            'in': 'query',
            'type': 'integer',
            'description': 'Filtrar por desarrolladora',
            'example': 1
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
    'description': '''Crea un nuevo videojuego con los datos proporcionados.
    
**Para asociar una desarrolladora**:
1. Usar GET /desarrolladoras para obtener la lista completa
2. Copiar el ID de la desarrolladora deseada
3. Incluir ese ID en el campo desarrolladora_id (opcional)

**Campos requeridos**: nombre, categoria, precio, valoracion
**Campos opcionales**: desarrolladora_id

**Ejemplo con desarrolladora**:
```json
{
    "nombre": "Nuevo Videojuego",
    "categoria": "RPG",
    "precio": 59.99,
    "valoracion": 9.2,
    "desarrolladora_id": 1
}
```''',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': '''Datos del videojuego a crear.

**Para usar desarrolladora_id**: 
- Primero consultar GET /desarrolladoras para ver las opciones
- Usar el ID numérico de la desarrolladora deseada
- El campo es opcional, puede omitirse''',
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

busqueda_avanzada_schema = {
    'tags': ['Videojuegos'],
    'summary': 'Búsqueda avanzada de videojuegos',
    'description': 'Realiza una búsqueda avanzada con múltiples filtros',
    'parameters': [
        {
            'name': 'categoria',
            'in': 'query',
            'type': 'string',
            'description': 'Filtrar por categoría',
            'example': 'RPG'
        },
        {
            'name': 'precio_min',
            'in': 'query',
            'type': 'number',
            'description': 'Precio mínimo',
            'example': 10.0
        },
        {
            'name': 'precio_max',
            'in': 'query',
            'type': 'number',
            'description': 'Precio máximo',
            'example': 60.0
        },
        {
            'name': 'valoracion_min',
            'in': 'query',
            'type': 'number',
            'description': 'Valoración mínima (0-10)',
            'example': 8.0
        },
        {
            'name': 'desarrolladora_id',
            'in': 'query',
            'type': 'integer',
            'description': 'ID de la desarrolladora',
            'example': 1
        },
        {
            'name': 'buscar',
            'in': 'query',
            'type': 'string',
            'description': 'Buscar en nombre, categoría y desarrolladora',
            'example': 'zelda'
        }
    ],
    'responses': {
        200: {
            'description': 'Búsqueda avanzada realizada exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Búsqueda avanzada realizada exitosamente con filtros: categoría: RPG, precio mín: $10.0'},
                    'data': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/Videojuego'}
                    },
                    'count': {'type': 'integer', 'example': 3},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {'$ref': '#/responses/BadRequest'},
        500: {'$ref': '#/responses/InternalServerError'}
    }
}

importar_externa_schema = {
    'tags': ['Videojuegos'],
    'summary': 'Importar videojuego desde RAWG',
    'description': 'Importa un videojuego desde RAWG API usando su external_id',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'external_id': {
                        'type': 'string',
                        'description': 'ID del juego en RAWG',
                        'example': '3328'
                    }
                },
                'required': ['external_id']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Juego importado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string'},
                    'data': {'$ref': '#/definitions/Videojuego'}
                }
            }
        },
        400: {'$ref': '#/responses/BadRequest'},
        503: {'description': 'Error en API externa'}
    }
}

importar_batch_schema = {
    'tags': ['Videojuegos'],
    'summary': 'Importar videojuegos desde RAWG',
    'description': '''Importa videojuegos desde RAWG API. Si no se proporcionan juegos en el body, importa automáticamente juegos populares evitando los que ya existen. Usa el parámetro "count" para especificar cuántos juegos importar.

Ejemplos de uso:

# 1. Sin parámetros (default: 6 juegos)
POST /api/videojuegos/importar-batch
Body: {}

# 2. Con parámetro count (importa 10 juegos populares)
POST /api/videojuegos/importar-batch?count=10
Body: {}

# 3. Con juegos específicos (ignora count)
POST /api/videojuegos/importar-batch?count=5
Body: {"games": [{"external_id": "3328"}]}''',
    'parameters': [
        {
            'name': 'count',
            'in': 'query',
            'type': 'integer',
            'description': 'Cantidad de juegos populares a importar (default: 6, máx: 50). Solo aplica si no se proporcionan juegos en el body.',
            'required': False,
            'default': 6,
            'minimum': 1,
            'maximum': 50,
            'example': 6
        },
        {
            'name': 'body',
            'in': 'body',
            'required': False,
            'schema': {
                'type': 'object',
                'properties': {
                    'games': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'external_id': {
                                    'type': 'string',
                                    'description': 'ID del juego en RAWG',
                                    'example': '3328'
                                }
                            },
                            'required': ['external_id']
                        },
                        'description': 'Lista de juegos a importar. Si no se proporciona, se importan automáticamente juegos populares (evitando los que ya existen).',
                        'example': [{'external_id': '3328'}, {'external_id': '3498'}]
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Juegos importados exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'success': {'type': 'array'},
                            'failed': {'type': 'array'},
                            'skipped': {'type': 'array'}
                        }
                    }
                }
            }
        },
        207: {'description': 'Multi-Status: algunos exitosos, algunos fallidos'},
        400: {'$ref': '#/responses/BadRequest'}
    }
}

get_enriquecido_schema = {
    'tags': ['Videojuegos'],
    'summary': 'Obtener videojuego enriquecido',
    'description': 'Obtiene un videojuego con datos adicionales de RAWG (screenshots, plataformas, tags)',
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
            'description': 'Juego enriquecido obtenido exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'nombre': {'type': 'string'},
                            'screenshots': {'type': 'array', 'items': {'type': 'string'}},
                            'plataformas': {'type': 'array', 'items': {'type': 'string'}},
                            'tags': {'type': 'array', 'items': {'type': 'string'}}
                        }
                    }
                }
            }
        },
        404: {'$ref': '#/responses/NotFound'}
    }
}

buscar_hibrida_schema = {
    'tags': ['Videojuegos'],
    'summary': 'Búsqueda híbrida',
    'description': 'Busca videojuegos en BD local y opcionalmente en RAWG',
    'parameters': [
        {
            'name': 'q',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Término de búsqueda',
            'example': 'zelda'
        },
        {
            'name': 'include_external',
            'in': 'query',
            'type': 'boolean',
            'description': 'Incluir resultados de RAWG',
            'example': True
        }
    ],
    'responses': {
        200: {
            'description': 'Búsqueda completada',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'local': {'type': 'array', 'items': {'$ref': '#/definitions/Videojuego'}},
                            'external': {'type': 'array'}
                        }
                    },
                    'count': {'type': 'integer'}
                }
            }
        },
        400: {'$ref': '#/responses/BadRequest'}
    }
}

sync_manual_schema = {
    'tags': ['Videojuegos'],
    'summary': 'Iniciar sincronización asíncrona',
    'description': 'Inicia una sincronización asíncrona de un juego desde RAWG',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'external_id': {
                        'type': 'string',
                        'description': 'ID del juego en RAWG',
                        'example': '3328'
                    }
                },
                'required': ['external_id']
            }
        }
    ],
    'responses': {
        202: {
            'description': 'Sincronización iniciada',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'task_id': {'type': 'string'},
                            'status_url': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {'$ref': '#/responses/BadRequest'}
    }
}

sync_status_schema = {
    'tags': ['Videojuegos'],
    'summary': 'Consultar estado de sincronización',
    'description': 'Consulta el estado de una tarea de sincronización asíncrona',
    'parameters': [
        {
            'name': 'task_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID de la tarea de Celery',
            'example': 'abc123-def456-ghi789'
        }
    ],
    'responses': {
        200: {
            'description': 'Estado de la sincronización',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'enum': ['pending', 'running', 'completed', 'failed']},
                            'result': {'type': 'object'},
                            'error': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
}