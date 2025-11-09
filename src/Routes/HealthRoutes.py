"""
Rutas para health check y estado del sistema.
"""
from flask import Blueprint, jsonify, current_app
from src.Config.Cache import cache

health_bp = Blueprint('health', __name__, url_prefix='/api/health')

@health_bp.route('', methods=['GET'])
def health_check():
    """
    Endpoint de health check que verifica el estado de los servicios.
    
    Returns:
        JSON con el estado de la aplicación, base de datos y Redis
    """
    status = {
        'status': 'ok',
        'services': {}
    }
    
    # Verificar Redis/Caché
    try:
        cache_type = current_app.config.get('CACHE_TYPE', 'unknown')
        status['services']['cache'] = {
            'type': cache_type,
            'status': 'connected' if cache_type == 'redis' else 'memory'
        }
        
        # Si es Redis, intentar hacer ping
        if cache_type == 'redis':
            try:
                cache.cache._write_client.ping()
                status['services']['cache']['status'] = 'connected'
                status['services']['cache']['ping'] = 'ok'
            except Exception as e:
                status['services']['cache']['status'] = 'disconnected'
                status['services']['cache']['error'] = str(e)
                status['status'] = 'degraded'
    except Exception as e:
        status['services']['cache'] = {
            'status': 'error',
            'error': str(e)
        }
        status['status'] = 'degraded'
    
    # Verificar base de datos
    try:
        from src.Config.Database import db
        # Intentar una consulta simple
        db.session.execute(db.text('SELECT 1'))
        status['services']['database'] = {
            'status': 'connected'
        }
    except Exception as e:
        status['services']['database'] = {
            'status': 'disconnected',
            'error': str(e)
        }
        status['status'] = 'error'
    
    # Determinar código de estado HTTP
    http_status = 200
    if status['status'] == 'error':
        http_status = 503
    elif status['status'] == 'degraded':
        http_status = 200  # Funciona pero con servicios degradados
    
    return jsonify(status), http_status

@health_bp.route('/redis', methods=['GET'])
def redis_check():
    """
    Endpoint específico para verificar el estado de Redis.
    
    Returns:
        JSON con el estado detallado de Redis
    """
    try:
        cache_type = current_app.config.get('CACHE_TYPE', 'unknown')
        
        if cache_type == 'redis':
            # Intentar hacer ping a Redis
            cache.cache._write_client.ping()
            
            # Obtener información de Redis
            redis_info = {
                'status': 'connected',
                'type': 'redis',
                'url': current_app.config.get('CACHE_REDIS_URL', 'not configured'),
                'ping': 'ok'
            }
            
            # Intentar obtener información adicional
            try:
                info = cache.cache._write_client.info()
                redis_info['redis_version'] = info.get('redis_version', 'unknown')
                redis_info['connected_clients'] = info.get('connected_clients', 0)
            except:
                pass
            
            return jsonify(redis_info), 200
        else:
            return jsonify({
                'status': 'using_memory_cache',
                'type': cache_type,
                'message': 'Redis no configurado, usando caché en memoria'
            }), 200
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'type': current_app.config.get('CACHE_TYPE', 'unknown')
        }), 503

