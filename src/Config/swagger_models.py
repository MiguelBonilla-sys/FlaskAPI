from flask_restx import fields

def create_swagger_models(api):
    """Crea los modelos de Swagger para la documentación de la API"""
    
    # Modelo para crear un videojuego (entrada)
    videojuego_input = api.model('VideojuegoInput', {
        'nombre': fields.String(
            required=True,
            description='Nombre del videojuego',
            example='The Legend of Zelda: Breath of the Wild'
        ),
        'categoria': fields.String(
            required=True,
            description='Categoría del videojuego',
            example='Aventura'
        ),
        'precio': fields.Float(
            required=True,
            description='Precio del videojuego en USD',
            example=59.99,
            min=0
        ),
        'valoracion': fields.Float(
            required=True,
            description='Valoración del videojuego (0-10)',
            example=9.7,
            min=0,
            max=10
        )
    })
    
    # Modelo para actualizar un videojuego (entrada parcial)
    videojuego_update = api.model('VideojuegoUpdate', {
        'nombre': fields.String(
            description='Nombre del videojuego',
            example='The Legend of Zelda: Breath of the Wild'
        ),
        'categoria': fields.String(
            description='Categoría del videojuego',
            example='Aventura'
        ),
        'precio': fields.Float(
            description='Precio del videojuego en USD',
            example=59.99,
            min=0
        ),
        'valoracion': fields.Float(
            description='Valoración del videojuego (0-10)',
            example=9.7,
            min=0,
            max=10
        )
    })
    
    # Modelo para respuesta de videojuego (salida)
    videojuego_output = api.model('VideojuegoOutput', {
        'id': fields.Integer(
            description='ID único del videojuego',
            example=1
        ),
        'nombre': fields.String(
            description='Nombre del videojuego',
            example='The Legend of Zelda: Breath of the Wild'
        ),
        'categoria': fields.String(
            description='Categoría del videojuego',
            example='Aventura'
        ),
        'precio': fields.Float(
            description='Precio del videojuego en USD',
            example=59.99
        ),
        'valoracion': fields.Float(
            description='Valoración del videojuego (0-10)',
            example=9.7
        ),
        'fecha_creacion': fields.String(
            description='Fecha de creación en formato ISO',
            example='2024-08-30T10:30:00.123456'
        ),
        'fecha_actualizacion': fields.String(
            description='Fecha de última actualización en formato ISO',
            example='2024-08-30T10:30:00.123456'
        )
    })
    
    # Modelo para respuesta exitosa
    api_response = api.model('ApiResponse', {
        'success': fields.Boolean(
            description='Indica si la operación fue exitosa',
            example=True
        ),
        'message': fields.String(
            description='Mensaje descriptivo de la operación',
            example='Operación realizada exitosamente'
        ),
        'timestamp': fields.String(
            description='Timestamp de la respuesta en formato ISO',
            example='2024-08-30T10:30:00.123456'
        )
    })
    
    # Modelo para respuesta con datos de videojuego
    videojuego_response = api.model('VideojuegoResponse', {
        'success': fields.Boolean(
            description='Indica si la operación fue exitosa',
            example=True
        ),
        'message': fields.String(
            description='Mensaje descriptivo de la operación',
            example='Videojuego encontrado'
        ),
        'data': fields.Nested(videojuego_output),
        'timestamp': fields.String(
            description='Timestamp de la respuesta en formato ISO',
            example='2024-08-30T10:30:00.123456'
        )
    })
    
    # Modelo para respuesta con lista de videojuegos
    videojuegos_list_response = api.model('VideojuegosListResponse', {
        'success': fields.Boolean(
            description='Indica si la operación fue exitosa',
            example=True
        ),
        'message': fields.String(
            description='Mensaje descriptivo de la operación',
            example='Lista de videojuegos'
        ),
        'data': fields.List(fields.Nested(videojuego_output)),
        'count': fields.Integer(
            description='Número de videojuegos en la lista',
            example=5
        ),
        'timestamp': fields.String(
            description='Timestamp de la respuesta en formato ISO',
            example='2024-08-30T10:30:00.123456'
        )
    })
    
    # Modelo para respuesta de error
    error_response = api.model('ErrorResponse', {
        'success': fields.Boolean(
            description='Indica si la operación fue exitosa',
            example=False
        ),
        'message': fields.String(
            description='Mensaje de error',
            example='Error al procesar la solicitud'
        ),
        'timestamp': fields.String(
            description='Timestamp de la respuesta en formato ISO',
            example='2024-08-30T10:30:00.123456'
        )
    })
    
    # Modelo para información de la API
    api_info = api.model('ApiInfo', {
        'nombre': fields.String(
            description='Nombre de la API',
            example='API de Videojuegos'
        ),
        'version': fields.String(
            description='Versión de la API',
            example='1.0.0'
        ),
        'descripcion': fields.String(
            description='Descripción de la API',
            example='API REST para gestionar videojuegos con operaciones CRUD'
        ),
        'endpoints': fields.Raw(
            description='Lista de endpoints disponibles'
        )
    })
    
    api_info_response = api.model('ApiInfoResponse', {
        'success': fields.Boolean(
            description='Indica si la operación fue exitosa',
            example=True
        ),
        'message': fields.String(
            description='Mensaje descriptivo',
            example='API de Videojuegos funcionando correctamente'
        ),
        'data': fields.Nested(api_info),
        'timestamp': fields.String(
            description='Timestamp de la respuesta en formato ISO',
            example='2024-08-30T10:30:00.123456'
        )
    })
    
    return {
        'videojuego_input': videojuego_input,
        'videojuego_update': videojuego_update,
        'videojuego_output': videojuego_output,
        'api_response': api_response,
        'videojuego_response': videojuego_response,
        'videojuegos_list_response': videojuegos_list_response,
        'error_response': error_response,
        'api_info_response': api_info_response
    }
