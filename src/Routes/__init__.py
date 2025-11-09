"""
Registro y configuración de todos los blueprints de la aplicación.
"""
from .ApiRoutes import api_bp
from .VideojuegosRoutes import videojuegos_bp
from .DesarrolladorasRoutes import desarrolladoras_bp
from .HealthRoutes import health_bp
from .SyncLogRoutes import sync_logs_bp

def register_blueprints(app):
    """
    Registra todos los blueprints en la aplicación.
    
    Args:
        app: Instancia de Flask
    """
    app.register_blueprint(api_bp)
    app.register_blueprint(videojuegos_bp)
    app.register_blueprint(desarrolladoras_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(sync_logs_bp)

def get_all_blueprints():
    """
    Retorna todos los blueprints de la aplicación.
    
    Returns:
        list: Lista de blueprints
    """
    return [api_bp, videojuegos_bp, desarrolladoras_bp]

__all__ = ['register_blueprints', 'get_all_blueprints']
