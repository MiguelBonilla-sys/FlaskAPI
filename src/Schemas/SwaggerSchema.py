"""
Esquemas y definiciones comunes reutilizables para Swagger.
"""

def get_swagger_definitions():
    """
    Retorna las definiciones de modelos para Swagger.
    
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
                'desarrolladora_id': {'type': 'integer', 'example': 1},
                'desarrolladora': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'nombre': {'type': 'string', 'example': 'Nintendo'},
                        'pais': {'type': 'string', 'example': 'Japón'},
                        'fundacion': {'type': 'integer', 'example': 18890923, 'description': 'Fecha de fundación en formato YYYYMMDD'},
                        'sitio_web': {'type': 'string', 'example': 'https://www.nintendo.com'},
                        'descripcion': {'type': 'string', 'example': 'Compañía japonesa de videojuegos conocida por Mario, Zelda y Pokémon'}
                    }
                },
                'fecha_creacion': {'type': 'string', 'format': 'date-time'},
                'fecha_actualizacion': {'type': 'string', 'format': 'date-time'}
            }
        },
        'VideojuegoInput': {
            'type': 'object',
            'required': ['nombre', 'categoria', 'precio', 'valoracion'],
            'properties': {
                'nombre': {
                    'type': 'string', 
                    'example': 'The Witcher 3: Wild Hunt',
                    'minLength': 1,
                    'maxLength': 255
                },
                'categoria': {
                    'type': 'string', 
                    'example': 'RPG',
                    'minLength': 1,
                    'maxLength': 100
                },
                'precio': {
                    'type': 'number', 
                    'format': 'float', 
                    'minimum': 0, 
                    'example': 39.99
                },
                'valoracion': {
                    'type': 'number', 
                    'format': 'float', 
                    'minimum': 0, 
                    'maximum': 10, 
                    'example': 9.3
                },
                'desarrolladora_id': {
                    'type': 'integer',
                    'description': 'ID de la desarrolladora que desarrolló el videojuego (opcional). Usar GET /desarrolladoras para ver las opciones disponibles.'
                }
            },
            'example': {
                'nombre': 'Nuevo Videojuego',
                'categoria': 'Aventura', 
                'precio': 49.99,
                'valoracion': 8.5
            }
        },
        'VideojuegoUpdateInput': {
            'type': 'object',
            'properties': {
                'nombre': {
                    'type': 'string', 
                    'example': 'The Witcher 3: Wild Hunt - Complete Edition',
                    'minLength': 1,
                    'maxLength': 255
                },
                'categoria': {
                    'type': 'string', 
                    'example': 'RPG',
                    'minLength': 1,
                    'maxLength': 100
                },
                'precio': {
                    'type': 'number', 
                    'format': 'float', 
                    'minimum': 0, 
                    'example': 29.99
                },
                'valoracion': {
                    'type': 'number', 
                    'format': 'float', 
                    'minimum': 0, 
                    'maximum': 10, 
                    'example': 9.5
                },
                'desarrolladora_id': {
                    'type': 'integer',
                    'description': 'ID de la desarrolladora que desarrolló el videojuego (opcional). Usar GET /desarrolladoras para ver las opciones disponibles.'
                }
            }
        },
        'ApiResponse': {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'message': {'type': 'string'},
                'data': {'type': 'object'},
                'count': {'type': 'integer'},
                'timestamp': {'type': 'string', 'format': 'date-time'}
            }
        },
        'ErrorResponse': {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean', 'example': False},
                'message': {'type': 'string'},
                'errors': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
                'timestamp': {'type': 'string', 'format': 'date-time'}
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
            'description': 'Petición incorrecta - Error en validación',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': 'Error en la validación de datos'},
                    'errors': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'example': ['El nombre es requerido', 'El precio debe ser mayor a 0']
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
        },
        'Desarrolladora': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer', 'example': 1},
                'nombre': {'type': 'string', 'example': 'Nintendo'},
                'pais': {'type': 'string', 'example': 'Japón'},
                'fundacion': {'type': 'integer', 'example': 18890923, 'description': 'Fecha de fundación en formato YYYYMMDD'},
                'sitio_web': {'type': 'string', 'example': 'https://www.nintendo.com'},
                'descripcion': {'type': 'string', 'example': 'Empresa japonesa de videojuegos fundada en 1889.'},
                'fecha_creacion': {'type': 'string', 'format': 'date-time'},
                'fecha_actualizacion': {'type': 'string', 'format': 'date-time'}
            }
        },
        'DesarrolladoraInput': {
            'type': 'object',
            'required': ['nombre'],
            'properties': {
                'nombre': {
                    'type': 'string',
                    'example': 'Capcom',
                    'minLength': 1,
                    'maxLength': 100
                },
                'pais': {
                    'type': 'string',
                    'example': 'Japón',
                    'maxLength': 100
                },
                'fundacion': {
                    'type': 'integer',
                    'example': 19790530,
                    'description': 'Fecha de fundación en formato YYYYMMDD'
                },
                'sitio_web': {
                    'type': 'string',
                    'example': 'https://www.capcom.com',
                    'maxLength': 200
                },
                'descripcion': {
                    'type': 'string',
                    'example': 'Desarrolladora y editora japonesa de videojuegos.'
                }
            }
        },
        'DesarrolladoraUpdateInput': {
            'type': 'object',
            'properties': {
                'nombre': {
                    'type': 'string',
                    'example': 'Capcom Co., Ltd.',
                    'minLength': 1,
                    'maxLength': 100
                },
                'pais': {
                    'type': 'string',
                    'example': 'Japón',
                    'maxLength': 100
                },
                'fundacion': {
                    'type': 'string',
                    'format': 'date',
                    'example': '1979-05-30',
                    'description': 'Fecha de fundación en formato YYYY-MM-DD'
                },
                'sitio_web': {
                    'type': 'string',
                    'example': 'https://www.capcom.com',
                    'maxLength': 200
                },
                'descripcion': {
                    'type': 'string',
                    'example': 'Desarrolladora y editora japonesa de videojuegos con sede en Osaka.'
                }
            }
        },
        'SuccessResponse': {
            'description': 'Operación exitosa',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string'},
                    'data': {'type': 'object'},
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        }
    }
