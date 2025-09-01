"""
Script auxiliar para detectar información del entorno Railway.
"""
import os
from urllib.parse import urlparse

def detect_railway_url():
    """
    Detecta la URL pública de Railway de múltiples formas.
    
    Returns:
        str: URL pública si se detecta, None en caso contrario
    """
    # Método 1: Variables de entorno directas
    direct_vars = [
        'RAILWAY_PUBLIC_DOMAIN',
        'RAILWAY_STATIC_URL', 
        'PUBLIC_URL'
    ]
    
    for var in direct_vars:
        url = os.getenv(var)
        if url:
            return url
    
    # Método 2: Construir desde variables de Railway
    service_name = os.getenv('RAILWAY_SERVICE_NAME')
    environment = os.getenv('RAILWAY_ENVIRONMENT')
    
    if service_name and environment:
        # Formato típico de Railway
        constructed_url = f"https://{service_name}-{environment}.up.railway.app"
        return constructed_url
    
    # Método 3: Si estamos en Railway pero no podemos detectar el dominio
    if os.getenv('RAILWAY_ENVIRONMENT'):
        print("⚠️ Detectado entorno Railway pero no se pudo determinar la URL pública")
        print("Variables disponibles:")
        railway_vars = {k: v for k, v in os.environ.items() if 'RAILWAY' in k}
        for key, value in railway_vars.items():
            print(f"  {key}: {value}")
    
    return None

def get_swagger_host():
    """
    Obtiene el host correcto para Swagger.
    
    Returns:
        tuple: (host, schemes)
    """
    # Detectar URL de Railway
    railway_url = detect_railway_url()
    
    if railway_url:
        # Limpiar la URL para obtener solo el host
        parsed = urlparse(railway_url if railway_url.startswith('http') else f'https://{railway_url}')
        host = parsed.netloc or railway_url.replace('https://', '').replace('http://', '')
        schemes = ["https", "http"]
        print(f"✅ [Railway] Host detectado: {host}")
        return host, schemes
    else:
        # Desarrollo local
        port = os.getenv('PORT', '5000')
        host = f"localhost:{port}"
        schemes = ["http", "https"]
        print(f"🏠 [Local] Host configurado: {host}")
        return host, schemes

if __name__ == "__main__":
    # Test del detector
    host, schemes = get_swagger_host()
    print(f"Host: {host}")
    print(f"Schemes: {schemes}")
