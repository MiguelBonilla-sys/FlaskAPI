from flask import jsonify, request
from typing import Any, Dict, Optional

def create_response(
    success: bool,
    message: str,
    data: Optional[Any] = None,
    status_code: int = 200
) -> tuple:
    """
    Crea una respuesta estandarizada para la API (para rutas normales de Flask)
    
    Args:
        success: Si la operación fue exitosa
        message: Mensaje descriptivo
        data: Datos a retornar (opcional)
        status_code: Código de estado HTTP
    
    Returns:
        Tuple con la respuesta JSON y el código de estado
    """
    response = {
        'success': success,
        'message': message,
        'timestamp': get_current_timestamp()
    }
    
    if data is not None:
        if isinstance(data, list):
            response['data'] = data
            response['count'] = len(data)
        else:
            response['data'] = data
    
    return jsonify(response), status_code

def create_json_response(
    success: bool,
    message: str,
    data: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Crea una respuesta JSON estandarizada para Flask-RESTX
    
    Args:
        success: Si la operación fue exitosa
        message: Mensaje descriptivo
        data: Datos a retornar (opcional)
    
    Returns:
        Diccionario con la respuesta JSON
    """
    response = {
        'success': success,
        'message': message,
        'timestamp': get_current_timestamp()
    }
    
    if data is not None:
        if isinstance(data, list):
            response['data'] = data
            response['count'] = len(data)
        else:
            response['data'] = data
    
    return response

def validate_json(request_obj) -> bool:
    """
    Valida que el request contenga JSON válido
    
    Args:
        request_obj: Objeto request de Flask
    
    Returns:
        True si el request contiene JSON válido, False caso contrario
    """
    try:
        if not request_obj.is_json:
            return False
        
        data = request_obj.get_json()
        return data is not None
    
    except Exception:
        return False

def get_current_timestamp() -> str:
    """
    Obtiene el timestamp actual en formato ISO
    
    Returns:
        String con el timestamp actual
    """
    from datetime import datetime
    return datetime.now().isoformat()

def extract_pagination_params(request_obj, default_page: int = 1, default_limit: int = 10):
    """
    Extrae parámetros de paginación del request
    
    Args:
        request_obj: Objeto request de Flask
        default_page: Página por defecto
        default_limit: Límite por defecto
    
    Returns:
        Tuple con (página, límite)
    """
    try:
        page = int(request_obj.args.get('page', default_page))
        limit = int(request_obj.args.get('limit', default_limit))
        
        # Validar que sean valores positivos
        page = max(1, page)
        limit = max(1, min(100, limit))  # Máximo 100 items por página
        
        return page, limit
    
    except (ValueError, TypeError):
        return default_page, default_limit