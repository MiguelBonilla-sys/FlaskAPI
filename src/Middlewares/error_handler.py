"""
Middleware para el manejo de errores de la aplicación.
"""
from flask import jsonify, request
from werkzeug.exceptions import HTTPException
from src.Utils import create_error_response
from src.Middlewares.rate_limiter import setup_rate_limiting
from src.Middlewares.auth import setup_authentication
import logging

def register_error_handlers(app):
    """
    Registra todos los manejadores de error para la aplicación.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        """Maneja errores de petición incorrecta."""
        return create_error_response(
            message="Petición incorrecta",
            status_code=400,
            errors=[str(error.description) if hasattr(error, 'description') else "Datos inválidos"]
        )
    
    @app.errorhandler(404)
    def not_found(error):
        """Maneja errores de recurso no encontrado."""
        return create_error_response(
            message="Recurso no encontrado",
            status_code=404,
            errors=[f"La ruta '{request.path}' no existe"]
        )
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Maneja errores de método no permitido."""
        return create_error_response(
            message="Método no permitido",
            status_code=405,
            errors=[f"El método {request.method} no está permitido para la ruta '{request.path}'"]
        )
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        """Maneja errores de entidad no procesable."""
        return create_error_response(
            message="Entidad no procesable",
            status_code=422,
            errors=[str(error.description) if hasattr(error, 'description') else "Datos no válidos"]
        )
    
    @app.errorhandler(500)
    def internal_error(error):
        """Maneja errores internos del servidor."""
        # Log del error para debugging
        app.logger.error(f'Error interno del servidor: {str(error)}')
        
        return create_error_response(
            message="Error interno del servidor",
            status_code=500,
            errors=["Ha ocurrido un error inesperado en el servidor"]
        )
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Maneja todas las excepciones HTTP."""
        return create_error_response(
            message=error.name,
            status_code=error.code,
            errors=[error.description]
        )
    
    @app.errorhandler(Exception)
    def handle_general_exception(error):
        """Maneja excepciones generales no capturadas."""
        # Log del error para debugging
        app.logger.error(f'Excepción no capturada: {str(error)}', exc_info=True)
        
        # En producción, no mostrar detalles del error
        if app.config.get('DEBUG', False):
            error_detail = str(error)
        else:
            error_detail = "Ha ocurrido un error inesperado"
        
        return create_error_response(
            message="Error del servidor",
            status_code=500,
            errors=[error_detail]
        )

def setup_logging(app):
    """
    Configura el sistema de logging para la aplicación.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    if not app.debug:
        # Configurar logging para producción
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s'
        )
        
        # Configurar logger de la aplicación
        app.logger.setLevel(logging.INFO)
        app.logger.info('API de Videojuegos iniciada')

# Middleware para logging de requests
def log_request_info(app):
    """
    Configura logging de información de requests.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    
    @app.before_request
    def log_request():
        """Log información básica de cada request."""
        app.logger.info(f'{request.method} {request.path} - IP: {request.remote_addr}')
    
    @app.after_request
    def log_response(response):
        """Log información básica de cada response."""
        app.logger.info(f'Response: {response.status_code}')
        return response

def setup_cors(app):
    """
    Configura CORS básico para la aplicación.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    
    @app.after_request
    def after_request(response):
        """Agrega headers CORS a todas las respuestas."""
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-API-Key')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

def setup_security_middlewares(app):
    """
    Configura todos los middlewares de seguridad.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    # Configurar rate limiting
    setup_rate_limiting(app)
    
    # Configurar autenticación
    setup_authentication(app)
    
    # Configurar validación de entrada
    from src.Middlewares.input_validation import setup_input_validation
    setup_input_validation(app)
    
    # Headers de seguridad adicionales
    @app.after_request
    def add_security_headers(response):
        """Agrega headers de seguridad."""
        # Prevenir ataques de clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Prevenir MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Habilitar XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Política de referrer
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy básica
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        
        return response
    
    app.logger.info('Middlewares de seguridad configurados exitosamente')
