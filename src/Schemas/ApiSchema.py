"""
Esquemas de Swagger para rutas generales de la API.
"""

health_schema = {
    'tags': ['Sistema'],
    'summary': 'Health Check',
    'description': 'Verifica el estado de salud de la API',
    'responses': {
        200: {
            'description': 'API funcionando correctamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'API funcionando correctamente'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string', 'example': 'healthy'},
                            'version': {'type': 'string', 'example': 'v1'}
                        }
                    },
                    'timestamp': {'type': 'string', 'format': 'date-time'}
                }
            }
        }
    }
}

api_info_schema = {
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
}
