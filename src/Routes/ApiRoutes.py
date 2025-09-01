"""
Rutas generales del sistema (health check, info, etc.).
"""
from flask import Blueprint
from flasgger import swag_from
from src.Utils import get_api_info, create_response
from src.Schemas.ApiSchema import health_schema, api_info_schema
import os

# Crear blueprint para rutas generales
api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
@swag_from(health_schema)
def health():
    """Endpoint de verificación de salud de la aplicación."""
    return create_response(
        success=True,
        message="API funcionando correctamente",
        data={
            'status': 'healthy',
            'version': os.getenv('API_VERSION', 'v1')
        }
    )

@api_bp.route('/api/', methods=['GET'])
@swag_from(api_info_schema)
def get_api_info_route():
    """Endpoint para obtener información de la API."""
    return create_response(
        success=True,
        message="Información de la API obtenida exitosamente",
        data=get_api_info()
    )
