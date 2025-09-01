"""
Configuración principal de Swagger y exportación de esquemas.
"""
import os

def get_swagger_config():
    """
    Retorna la configuración completa de Swagger.
    
    Returns:
        dict: Configuración de Swagger
    """
    return {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

def get_swagger_template():
    """
    Retorna el template base de Swagger.
    
    Returns:
        dict: Template de Swagger
    """
    from src.Schemas.SwaggerSchema import get_swagger_definitions, get_swagger_responses
    
    # Detectar el host dinámicamente con múltiples métodos
    def detect_host_and_schemes():
        """Detecta el host y esquemas correctos para Swagger."""
        
        # Método 1: Variables de entorno directas de Railway
        railway_vars = [
            'RAILWAY_PUBLIC_DOMAIN',
            'RAILWAY_STATIC_URL', 
            'PUBLIC_URL'
        ]
        
        for var in railway_vars:
            url = os.getenv(var)
            if url:
                host = url.replace('https://', '').replace('http://', '')
                return host, ["https", "http"]
        
        # Método 2: Construir desde variables de Railway
        service_name = os.getenv('RAILWAY_SERVICE_NAME')
        environment = os.getenv('RAILWAY_ENVIRONMENT')
        
        if service_name and environment:
            host = f"{service_name}-{environment}.up.railway.app"
            return host, ["https", "http"]
        
        # Método 3: Detectar Railway por otras variables
        if os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('RAILWAY_PROJECT_ID'):
            # Estamos en Railway, usar tu dominio conocido
            host = "flaskapi-production-badd.up.railway.app"
            print(f"⚠️ [Railway] Usando dominio conocido: {host}")
            return host, ["https", "http"]
        
        # Método 4: Desarrollo local
        port = os.getenv('PORT', '5000')
        host = f"localhost:{port}"
        return host, ["http", "https"]
    
    # Obtener host y esquemas
    host, schemes = detect_host_and_schemes()
    print(f"🌐 [Swagger] Host configurado: {host} | Schemes: {schemes}")
    
    return {
        "swagger": "2.0",
        "info": {
            "title": "Videojuegos API",
            "description": "API REST para gestión de videojuegos",
            "version": "v1",
            "contact": {
                "name": "API Support",
                "email": "support@videojuegosapi.com"
            },
            "license": {
                "name": "MIT License",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "host": host,
        "basePath": "/",
        "schemes": schemes,
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "definitions": get_swagger_definitions(),
        "responses": get_swagger_responses(),
        "tags": [
            {
                "name": "Sistema",
                "description": "Endpoints del sistema y health checks"
            },
            {
                "name": "API Info",
                "description": "Información general de la API"
            },
            {
                "name": "Videojuegos",
                "description": "Operaciones CRUD para videojuegos"
            }
        ]
    }

# Importaciones desde otros módulos para exportación
from src.Schemas.SwaggerSchema import get_swagger_definitions, get_swagger_responses
from src.Schemas.ApiSchema import health_schema, api_info_schema
from src.Schemas.VideojuegosSchema import (
    get_videojuegos_schema,
    get_videojuego_schema,
    create_videojuego_schema,
    update_videojuego_schema,
    delete_videojuego_schema,
    get_categorias_schema,
    get_estadisticas_schema
)

__all__ = [
    'get_swagger_config',
    'get_swagger_template',
    'get_swagger_definitions',
    'get_swagger_responses',
    'health_schema',
    'api_info_schema',
    'get_videojuegos_schema',
    'get_videojuego_schema',
    'create_videojuego_schema',
    'update_videojuego_schema',
    'delete_videojuego_schema',
    'get_categorias_schema',
    'get_estadisticas_schema'
]
