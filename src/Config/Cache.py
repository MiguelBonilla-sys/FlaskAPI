"""
Configuración de caché con Redis para Flask-Caching.
"""
import os
import re
from flask_caching import Cache

cache = Cache()

def _clean_redis_url(url):
    """
    Limpia la URL de Redis removiendo comentarios y espacios.
    
    Args:
        url: URL de Redis que puede contener comentarios o texto adicional
    
    Returns:
        str: URL limpia de Redis
    """
    if not url:
        return 'redis://localhost:6379/0'
    
    # Remover comentarios y texto después de paréntesis o espacios
    # Ejemplo: "redis://host:6379 (comentario)" -> "redis://host:6379"
    url = url.strip()
    
    # Si hay paréntesis, tomar solo la parte antes
    if '(' in url:
        url = url.split('(')[0].strip()
    
    # Remover espacios al final
    url = url.strip()
    
    # Validar formato básico
    if not url.startswith('redis://') and not url.startswith('rediss://'):
        # Si no es una URL válida, intentar construir desde variables individuales
        redis_host = os.getenv('REDISHOST', 'localhost')
        redis_port = os.getenv('REDISPORT', '6379')
        redis_user = os.getenv('REDISUSER', 'default')
        redis_password = os.getenv('REDISPASSWORD', '')
        
        if redis_password:
            url = f'redis://{redis_user}:{redis_password}@{redis_host}:{redis_port}/0'
        else:
            url = f'redis://{redis_host}:{redis_port}/0'
    
    return url

def init_cache(app):
    """
    Inicializa Flask-Caching con Redis o caché en memoria para tests.
    Si Redis no está disponible, usa caché simple en memoria.
    
    Args:
        app: Instancia de Flask
    """
    # En modo test, usar caché en memoria (no requiere Redis)
    if app.config.get('TESTING', False) or os.getenv('FLASK_ENV') == 'testing':
        app.config['CACHE_TYPE'] = 'simple'  # Caché en memoria
        app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutos para tests
        cache.init_app(app)
    else:
        redis_url_raw = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        redis_url = _clean_redis_url(redis_url_raw)
        
        # Intentar usar Redis, si falla usar caché simple
        try:
            app.config['CACHE_TYPE'] = 'redis'
            app.config['CACHE_REDIS_URL'] = redis_url
            app.config['CACHE_DEFAULT_TIMEOUT'] = 3600  # 1 hora por defecto
            
            # Intentar inicializar para verificar conexión
            cache.init_app(app)
            
            # Verificar conexión haciendo una operación simple
            try:
                cache.cache._write_client.ping()
            except Exception:
                # Si no se puede conectar, usar caché simple
                app.config['CACHE_TYPE'] = 'simple'
                app.config['CACHE_DEFAULT_TIMEOUT'] = 3600
                cache.init_app(app)
                if app.config.get('DEBUG', False):
                    print("⚠️ Advertencia: Redis no disponible, usando caché en memoria")
        except Exception as e:
            # Si hay error al configurar Redis, usar caché simple
            app.config['CACHE_TYPE'] = 'simple'
            app.config['CACHE_DEFAULT_TIMEOUT'] = 3600
            cache.init_app(app)
            if app.config.get('DEBUG', False):
                print(f"⚠️ Advertencia: Error configurando Redis ({e}), usando caché en memoria")
    
    return cache

