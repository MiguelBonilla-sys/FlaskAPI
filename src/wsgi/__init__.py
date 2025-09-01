"""
Módulo WSGI para despliegue en producción.
"""
from .wsgi import application, app

__all__ = ['application', 'app']
