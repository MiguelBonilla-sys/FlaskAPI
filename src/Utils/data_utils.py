"""
Utilidades para manejo seguro de datos anidados.
"""

def safe_get(data, *keys, default=None):
    """
    Navega estructura anidada de forma segura.
    
    Args:
        data: Estructura de datos (dict, list, etc.)
        *keys: Claves/índices para navegar
        default: Valor por defecto si no se encuentra
    
    Returns:
        Valor encontrado o default
    
    Ejemplo:
        safe_get(data, 'price_overview', 'final', default=0)
        safe_get(data, 'genres', 0, 'name', default='Unknown')
    """
    current = data
    
    for key in keys:
        try:
            if isinstance(current, dict):
                current = current.get(key)
            elif isinstance(current, list) and isinstance(key, int):
                if 0 <= key < len(current):
                    current = current[key]
                else:
                    return default
            else:
                return default
            
            if current is None:
                return default
                
        except (KeyError, IndexError, TypeError, AttributeError):
            return default
    
    return current if current is not None else default

