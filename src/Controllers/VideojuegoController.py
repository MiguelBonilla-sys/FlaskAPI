from flask import request
from flasgger import swag_from
from src.Services.VideojuegoService import videojuego_service
from src.Utils import create_response, validate_json

class VideojuegoController:
    @staticmethod
    @swag_from({
        'tags': ['Videojuegos'],
        'summary': 'Obtener todos los videojuegos',
        'description': 'Obtiene una lista de todos los videojuegos con filtros opcionales',
        'parameters': [
            {
                'name': 'categoria',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Filtrar videojuegos por categoría'
            },
            {
                'name': 'buscar',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Buscar videojuegos por nombre o categoría'
            }
        ],
        'responses': {
            200: {
                'description': 'Lista de videojuegos obtenida exitosamente',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'success': {'type': 'boolean', 'example': True},
                        'message': {'type': 'string', 'example': 'Lista de todos los videojuegos'},
                        'data': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'id': {'type': 'integer', 'example': 1},
                                    'nombre': {'type': 'string', 'example': 'The Legend of Zelda'},
                                    'categoria': {'type': 'string', 'example': 'Aventura'},
                                    'precio': {'type': 'number', 'example': 59.99},
                                    'valoracion': {'type': 'number', 'example': 9.7},
                                    'fecha_creacion': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'},
                                    'fecha_actualizacion': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                                }
                            }
                        },
                        'count': {'type': 'integer', 'example': 5},
                        'timestamp': {'type': 'string', 'example': '2024-08-30T10:30:00.123456'}
                    }
                }
            },
            500: {
                'description': 'Error interno del servidor'
            }
        }
    })
    def get_all_videojuegos():
        """Obtiene todos los videojuegos con filtros opcionales"""
        try:
            # Parámetros de consulta opcionales
            categoria = request.args.get('categoria')
            buscar = request.args.get('buscar')
            
            if categoria:
                videojuegos = videojuego_service.get_videojuegos_by_categoria(categoria)
                message = f"Videojuegos de la categoría '{categoria}'"
            elif buscar:
                videojuegos = videojuego_service.search_videojuegos(buscar)
                message = f"Resultados de búsqueda para '{buscar}'"
            else:
                videojuegos = videojuego_service.get_all_videojuegos()
                message = "Lista de todos los videojuegos"
            
            return create_response(
                success=True,
                message=message,
                data=videojuegos,
                status_code=200
            )
        
        except Exception as e:
            return create_response(
                success=False,
                message=f"Error al obtener videojuegos: {str(e)}",
                status_code=500
            )
    
    @staticmethod
    @swag_from({
        'tags': ['Videojuegos'],
        'summary': 'Obtener videojuego por ID',
        'description': 'Obtiene un videojuego específico por su ID',
        'parameters': [
            {
                'name': 'game_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID del videojuego'
            }
        ],
        'responses': {
            200: {
                'description': 'Videojuego encontrado'
            },
            404: {
                'description': 'Videojuego no encontrado'
            }
        }
    })
    def get_videojuego_by_id(game_id):
        """Obtiene un videojuego específico por su ID"""
        try:
            videojuego = videojuego_service.get_videojuego_by_id(game_id)
            
            if not videojuego:
                return create_response(
                    success=False,
                    message=f"Videojuego con ID {game_id} no encontrado",
                    status_code=404
                )
            
            return create_response(
                success=True,
                message="Videojuego encontrado",
                data=videojuego,
                status_code=200
            )
        
        except Exception as e:
            return create_response(
                success=False,
                message=f"Error al obtener videojuego: {str(e)}",
                status_code=500
            )
    
    @staticmethod
    @swag_from({
        'tags': ['Videojuegos'],
        'summary': 'Crear nuevo videojuego',
        'description': 'Crea un nuevo videojuego en la base de datos',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'required': ['nombre', 'categoria', 'precio', 'valoracion'],
                    'properties': {
                        'nombre': {
                            'type': 'string',
                            'description': 'Nombre del videojuego',
                            'example': 'Cyberpunk 2077'
                        },
                        'categoria': {
                            'type': 'string',
                            'description': 'Categoría del videojuego',
                            'example': 'RPG'
                        },
                        'precio': {
                            'type': 'number',
                            'description': 'Precio en USD',
                            'example': 59.99,
                            'minimum': 0
                        },
                        'valoracion': {
                            'type': 'number',
                            'description': 'Valoración del 0 al 10',
                            'example': 8.5,
                            'minimum': 0,
                            'maximum': 10
                        }
                    }
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Videojuego creado exitosamente'
            },
            400: {
                'description': 'Datos inválidos'
            }
        }
    })
    def create_videojuego():
        """Crea un nuevo videojuego"""
        try:
            # Validar que el request tenga JSON
            if not validate_json(request):
                return create_response(
                    success=False,
                    message="Debe enviar datos en formato JSON",
                    status_code=400
                )
            
            data = request.get_json()
            videojuego = videojuego_service.create_videojuego(data)
            
            return create_response(
                success=True,
                message="Videojuego creado exitosamente",
                data=videojuego,
                status_code=201
            )
        
        except ValueError as e:
            return create_response(
                success=False,
                message=str(e),
                status_code=400
            )
        
        except Exception as e:
            return create_response(
                success=False,
                message=f"Error al crear videojuego: {str(e)}",
                status_code=500
            )
    
    @staticmethod
    @swag_from({
        'tags': ['Videojuegos'],
        'summary': 'Actualizar videojuego',
        'description': 'Actualiza un videojuego existente',
        'parameters': [
            {
                'name': 'game_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID del videojuego'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nombre': {
                            'type': 'string',
                            'description': 'Nombre del videojuego'
                        },
                        'categoria': {
                            'type': 'string',
                            'description': 'Categoría del videojuego'
                        },
                        'precio': {
                            'type': 'number',
                            'description': 'Precio en USD',
                            'minimum': 0
                        },
                        'valoracion': {
                            'type': 'number',
                            'description': 'Valoración del 0 al 10',
                            'minimum': 0,
                            'maximum': 10
                        }
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Videojuego actualizado exitosamente'
            },
            404: {
                'description': 'Videojuego no encontrado'
            },
            400: {
                'description': 'Datos inválidos'
            }
        }
    })
    def update_videojuego(game_id):
        """Actualiza un videojuego existente"""
        try:
            # Validar que el request tenga JSON
            if not validate_json(request):
                return create_response(
                    success=False,
                    message="Debe enviar datos en formato JSON",
                    status_code=400
                )
            
            data = request.get_json()
            videojuego = videojuego_service.update_videojuego(game_id, data)
            
            if not videojuego:
                return create_response(
                    success=False,
                    message=f"Videojuego con ID {game_id} no encontrado",
                    status_code=404
                )
            
            return create_response(
                success=True,
                message="Videojuego actualizado exitosamente",
                data=videojuego,
                status_code=200
            )
        
        except ValueError as e:
            return create_response(
                success=False,
                message=str(e),
                status_code=400
            )
        
        except Exception as e:
            return create_response(
                success=False,
                message=f"Error al actualizar videojuego: {str(e)}",
                status_code=500
            )
    
    @staticmethod
    @swag_from({
        'tags': ['Videojuegos'],
        'summary': 'Eliminar videojuego',
        'description': 'Elimina un videojuego de la base de datos',
        'parameters': [
            {
                'name': 'game_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID del videojuego a eliminar'
            }
        ],
        'responses': {
            200: {
                'description': 'Videojuego eliminado exitosamente'
            },
            404: {
                'description': 'Videojuego no encontrado'
            }
        }
    })
    def delete_videojuego(game_id):
        """Elimina un videojuego"""
        try:
            deleted = videojuego_service.delete_videojuego(game_id)
            
            if not deleted:
                return create_response(
                    success=False,
                    message=f"Videojuego con ID {game_id} no encontrado",
                    status_code=404
                )
            
            return create_response(
                success=True,
                message="Videojuego eliminado exitosamente",
                status_code=200
            )
        
        except Exception as e:
            return create_response(
                success=False,
                message=f"Error al eliminar videojuego: {str(e)}",
                status_code=500
            )
