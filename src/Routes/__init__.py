"""
Registro y configuración de todos los blueprints de la aplicación.
"""
from .ApiRoutes import api_bp
from .VideojuegosRoutes import videojuegos_bp

def register_blueprints(app):
    """
    Registra todos los blueprints en la aplicación.
    
    Args:
        app: Instancia de Flask
    """
    app.register_blueprint(api_bp)
    app.register_blueprint(videojuegos_bp)

def get_all_blueprints():
    """
    Retorna todos los blueprints de la aplicación.
    
    Returns:
        list: Lista de blueprints
    """
    return [api_bp, videojuegos_bp]

__all__ = ['register_blueprints', 'get_all_blueprints']
