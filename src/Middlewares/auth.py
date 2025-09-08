"""
Middleware de autenticación simple con API keys.
"""
import os
import secrets
import hashlib
import hmac
from functools import wraps
from flask import request, jsonify, current_app
from src.Utils import create_error_response
import logging

class SimpleAuthenticator:
    """
    Autenticador simple basado en API keys.
    """
    
    def __init__(self):
        """
        Inicializa el autenticador.
        """
        # API keys válidas (en producción, usar base de datos)
        self.api_keys = {
            # Admin key (acceso completo)
            os.getenv('ADMIN_API_KEY', 'admin_key_123'): {
                'role': 'admin',
                'permissions': ['read', 'write', 'delete', 'admin']
            },
            # Read-only key (solo lectura)
            os.getenv('READONLY_API_KEY', 'readonly_key_456'): {
                'role': 'readonly',
                'permissions': ['read']
            },
            # Writer key (lectura y escritura)
            os.getenv('WRITER_API_KEY', 'writer_key_789'): {
                'role': 'writer',
                'permissions': ['read', 'write']
            }
        }
    
    def generate_api_key(self, length=32):
        """
        Genera una nueva API key segura.
        
        Args:
            length (int): Longitud de la key
            
        Returns:
            str: Nueva API key
        """
        return secrets.token_urlsafe(length)
    
    def validate_api_key(self, api_key):
        """
        Valida una API key.
        
        Args:
            api_key (str): API key a validar
            
        Returns:
            dict or None: Información del usuario o None si es inválida
        """
        if not api_key:
            return None
            
        return self.api_keys.get(api_key)
    
    def check_permission(self, user_info, required_permission):
        """
        Verifica si un usuario tiene el permiso requerido.
        
        Args:
            user_info (dict): Información del usuario
            required_permission (str): Permiso requerido
            
        Returns:
            bool: True si tiene permiso, False si no
        """
        if not user_info:
            return False
            
        return required_permission in user_info.get('permissions', [])

# Instancia global del autenticador
authenticator = SimpleAuthenticator()

def get_api_key_from_request():
    """
    Extrae la API key del request.
    
    Returns:
        str or None: API key si existe
    """
    # Verificar header Authorization
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header[7:]  # Remover 'Bearer '
    
    # Verificar header X-API-Key
    api_key = request.headers.get('X-API-Key')
    if api_key:
        return api_key
    
    # Verificar parámetro de query (menos seguro, solo para testing)
    return request.args.get('api_key')

def require_api_key(required_permission='read'):
    """
    Decorador que requiere autenticación con API key.
    
    Args:
        required_permission (str): Permiso requerido
        
    Returns:
        function: Decorador
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Obtener API key
            api_key = get_api_key_from_request()
            
            if not api_key:
                current_app.logger.warning(
                    f'Acceso sin API key a {request.endpoint} desde {request.remote_addr}'
                )
                return create_error_response(
                    message="API key requerida",
                    status_code=401,
                    errors=[
                        "Debes proporcionar una API key válida",
                        "Usa el header 'Authorization: Bearer YOUR_KEY' o 'X-API-Key: YOUR_KEY'"
                    ]
                )
            
            # Validar API key
            user_info = authenticator.validate_api_key(api_key)
            if not user_info:
                current_app.logger.warning(
                    f'API key inválida: {api_key[:8]}... desde {request.remote_addr}'
                )
                return create_error_response(
                    message="API key inválida",
                    status_code=401,
                    errors=["La API key proporcionada no es válida"]
                )
            
            # Verificar permisos
            if not authenticator.check_permission(user_info, required_permission):
                current_app.logger.warning(
                    f'Permiso insuficiente: {user_info["role"]} intentó {required_permission} en {request.endpoint}'
                )
                return create_error_response(
                    message="Permisos insuficientes",
                    status_code=403,
                    errors=[
                        f"Tu rol '{user_info['role']}' no tiene permiso para '{required_permission}'",
                        f"Permisos disponibles: {', '.join(user_info['permissions'])}"
                    ]
                )
            
            # Agregar info del usuario al request
            request.user_info = user_info
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def optional_api_key():
    """
    Decorador que permite autenticación opcional.
    
    Returns:
        function: Decorador
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = get_api_key_from_request()
            
            if api_key:
                user_info = authenticator.validate_api_key(api_key)
                request.user_info = user_info
            else:
                request.user_info = None
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """
    Decorador que requiere permisos de administrador.
    
    Args:
        f (function): Función a decorar
        
    Returns:
        function: Función decorada
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return require_api_key('admin')(f)(*args, **kwargs)
    return decorated_function

def setup_authentication(app):
    """
    Configura la autenticación para la aplicación.
    
    Args:
        app: Instancia de Flask
    """
    
    @app.before_request
    def log_authentication():
        """Log información de autenticación."""
        api_key = get_api_key_from_request()
        if api_key:
            user_info = authenticator.validate_api_key(api_key)
            if user_info:
                app.logger.info(
                    f'Petición autenticada: {user_info["role"]} -> {request.method} {request.path}'
                )
    
    # Endpoint para generar nuevas API keys (solo para admins)
    @app.route('/api/admin/generate-key', methods=['POST'])
    @require_api_key('admin')
    def generate_new_api_key():
        """Genera una nueva API key (solo admins)."""
        new_key = authenticator.generate_api_key()
        
        current_app.logger.info(
            f'Nueva API key generada por {request.user_info["role"]}'
        )
        
        return jsonify({
            'success': True,
            'message': 'Nueva API key generada exitosamente',
            'data': {
                'api_key': new_key,
                'note': 'Guarda esta key de forma segura, no se mostrará nuevamente'
            }
        }), 201
    
    app.logger.info('Sistema de autenticación configurado exitosamente')

def get_public_endpoints():
    """
    Lista de endpoints que no requieren autenticación.
    
    Returns:
        list: Lista de endpoints públicos
    """
    return [
        '/health',
        '/api/',
        '/apidocs',
        '/apidocs/',
        '/apispec.json',
        '/flasgger_static',
        '/'
    ]
