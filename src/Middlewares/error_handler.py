from flask import jsonify, request
from src.Utils import create_response
import traceback

def register_error_handlers(app):
    """Registra los manejadores de errores para la aplicación"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return create_response(
            success=False,
            message="Solicitud incorrecta: Datos inválidos o malformados",
            status_code=400
        )
    
    @app.errorhandler(404)
    def not_found(error):
        return create_response(
            success=False,
            message="Recurso no encontrado",
            status_code=404
        )
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return create_response(
            success=False,
            message="Método HTTP no permitido para este endpoint",
            status_code=405
        )
    
    @app.errorhandler(500)
    def internal_error(error):
        return create_response(
            success=False,
            message="Error interno del servidor",
            status_code=500
        )
    
    @app.before_request
    def log_request_info():
        """Log información de la request (opcional para debugging)"""
        if app.debug:
            print(f"Request: {request.method} {request.url}")
            if request.is_json:
                print(f"JSON: {request.get_json()}")

def register_middlewares(app):
    """Registra todos los middlewares"""
    register_error_handlers(app)
