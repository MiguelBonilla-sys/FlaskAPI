"""
Configuración de Celery para tareas asíncronas.
"""
import os
import re
from celery import Celery
from celery.schedules import crontab

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
    url = url.strip()
    
    # Si hay paréntesis, tomar solo la parte antes
    if '(' in url:
        url = url.split('(')[0].strip()
    
    # Remover espacios al final
    url = url.strip()
    
    # Si no es una URL válida, intentar construir desde variables individuales
    if not url.startswith('redis://') and not url.startswith('rediss://'):
        redis_host = os.getenv('REDISHOST', 'localhost')
        redis_port = os.getenv('REDISPORT', '6379')
        redis_user = os.getenv('REDISUSER', 'default')
        redis_password = os.getenv('REDISPASSWORD', '')
        
        if redis_password:
            url = f'redis://{redis_user}:{redis_password}@{redis_host}:{redis_port}/0'
        else:
            url = f'redis://{redis_host}:{redis_port}/0'
    
    return url

def make_celery(app):
    """
    Crea y configura instancia de Celery.
    
    Args:
        app: Instancia de Flask
    
    Returns:
        Celery: Instancia configurada de Celery
    """
    # Limpiar URLs de Redis
    backend_url_raw = os.getenv('CELERY_RESULT_BACKEND', os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
    broker_url_raw = os.getenv('CELERY_BROKER_URL', os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
    
    backend_url = _clean_redis_url(backend_url_raw)
    broker_url = _clean_redis_url(broker_url_raw)
    
    celery = Celery(
        app.import_name,
        backend=backend_url,
        broker=broker_url
    )
    
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,  # 30 minutos
        task_soft_time_limit=25 * 60,  # 25 minutos
    )
    
    # Configurar Celery Beat schedule
    celery.conf.beat_schedule = {
        'sync-popular-games-daily': {
            'task': 'src.Tasks.sync_tasks.sync_popular_games',
            'schedule': crontab(hour=2, minute=0),  # 2 AM diariamente
        },
        'sync-incremental': {
            'task': 'src.Tasks.sync_tasks.sync_incremental',
            'schedule': crontab(minute=0, hour='*/6'),  # Cada 6 horas
        }
    }
    
    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context."""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

# Crear instancia de Celery (se inicializará con app en create_app)
celery = None

def init_celery(app):
    """
    Inicializa Celery con la app Flask.
    
    Args:
        app: Instancia de Flask
    
    Returns:
        Celery: Instancia de Celery
    """
    global celery
    celery = make_celery(app)
    return celery

# Exportar celery para uso en tasks
__all__ = ['celery', 'init_celery', 'make_celery']

