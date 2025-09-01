"""
Utilidades generales para la API.
"""
from datetime import datetime
from flask import jsonify
import os

def create_response(success=True, message="", data=None, count=None, status_code=200):
    """
    Crea una respuesta estándar para la API.
    
    Args:
        success (bool): Indica si la operación fue exitosa
        message (str): Mensaje descriptivo de la operación
        data: Datos a incluir en la respuesta
        count (int): Número de elementos (para listas)
        status_code (int): Código de estado HTTP
        
    Returns:
        tuple: (response, status_code)
    """
    response = {
        'success': success,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    
    if data is not None:
        response['data'] = data
        
    if count is not None:
        response['count'] = count
    
    return jsonify(response), status_code

def create_error_response(message, status_code=400, errors=None):
    """
    Crea una respuesta de error estándar.
    
    Args:
        message (str): Mensaje de error
        status_code (int): Código de estado HTTP
        errors (list): Lista de errores específicos
        
    Returns:
        tuple: (response, status_code)
    """
    response = {
        'success': False,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    
    if errors:
        response['errors'] = errors
    
    return jsonify(response), status_code

def get_api_info():
    """
    Obtiene información básica de la API.
    
    Returns:
        dict: Información de la API
    """
    return {
        'name': os.getenv('API_TITLE', 'Videojuegos API'),
        'version': os.getenv('API_VERSION', 'v1'),
        'description': os.getenv('API_DESCRIPTION', 'API REST para gestión de videojuegos'),
        'endpoints': {
            'info': 'GET /api/',
            'swagger': 'GET /apidocs/',
            'videojuegos': {
                'list': 'GET /api/videojuegos',
                'create': 'POST /api/videojuegos',
                'get': 'GET /api/videojuegos/{id}',
                'update': 'PUT /api/videojuegos/{id}',
                'delete': 'DELETE /api/videojuegos/{id}'
            }
        }
    }

def validate_pagination_params(page=1, per_page=10):
    """
    Valida y normaliza parámetros de paginación.
    
    Args:
        page (int): Número de página
        per_page (int): Elementos por página
        
    Returns:
        tuple: (page, per_page)
    """
    try:
        page = max(1, int(page))
    except (ValueError, TypeError):
        page = 1
        
    try:
        per_page = max(1, min(100, int(per_page)))  # Máximo 100 elementos por página
    except (ValueError, TypeError):
        per_page = 10
        
    return page, per_page

def clean_string(value):
    """
    Limpia y normaliza una cadena de texto.
    
    Args:
        value (str): Cadena a limpiar
        
    Returns:
        str: Cadena limpia
    """
    if not value:
        return ""
    return str(value).strip()

def is_valid_number(value, min_val=None, max_val=None):
    """
    Valida si un valor es un número válido dentro de un rango.
    
    Args:
        value: Valor a validar
        min_val: Valor mínimo permitido
        max_val: Valor máximo permitido
        
    Returns:
        bool: True si es válido, False en caso contrario
    """
    try:
        num = float(value)
        if min_val is not None and num < min_val:
            return False
        if max_val is not None and num > max_val:
            return False
        return True
    except (ValueError, TypeError):
        return False
