"""
Tasks de Celery para sincronización de juegos desde RAWG.
"""
from celery import shared_task, group
from datetime import datetime, timedelta
from flask import current_app
from src.Config.Database import db
from src.Models.Videojuego import Videojuego
from src.Models.SyncLog import SyncLog
from src.Services.GameService import GameService
import logging
import time

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def sync_game_from_api(self, external_id):
    """
    Sincroniza un juego individual desde RAWG.
    
    Args:
        external_id: ID del juego en RAWG
    
    Returns:
        dict: Resultado de la sincronización
    """
    from app import create_app
    
    app = create_app()
    with app.app_context():
        # Crear registro de sincronización
        sync_log = SyncLog(external_id=str(external_id), api_source='rawg', status='pending')
        db.session.add(sync_log)
        db.session.commit()
        
        start_time = time.time()
        
        try:
            game_service = GameService()
            # No crear otro sync_log porque ya lo creamos arriba
            game = game_service.import_game(str(external_id), force_refresh=True, create_sync_log=False)
            
            # Marcar como exitoso (el sync_log ya fue creado arriba)
            duration = time.time() - start_time
            sync_log.mark_success(videojuego_id=game.id, duration_seconds=duration)
            db.session.commit()
            
            logger.info(f"Game {external_id} synced successfully")
            return {
                'status': 'success',
                'game_id': game.id,
                'external_id': external_id,
                'sync_log_id': sync_log.id
            }
            
        except Exception as e:
            # Marcar como fallido (el sync_log ya fue creado arriba)
            duration = time.time() - start_time
            error_msg = str(e)
            sync_log.mark_failed(error_message=error_msg, duration_seconds=duration)
            db.session.commit()
            
            logger.error(f"Error syncing game {external_id}: {e}")
            # Retry con backoff exponencial
            raise self.retry(exc=e, countdown=2 ** self.request.retries)

@shared_task
def sync_batch_games(games_list):
    """
    Sincroniza múltiples juegos en paralelo.
    
    Args:
        games_list: Lista de dicts con 'external_id'
    
    Returns:
        dict: Resultado del grupo de tasks
    """
    # Crear grupo de tasks paralelas
    job = group([
        sync_game_from_api.s(game_data.get('external_id'))
        for game_data in games_list
    ])
    
    result = job.apply_async()
    return {
        'task_group_id': result.id,
        'total_tasks': len(games_list)
    }

@shared_task
def sync_popular_games():
    """
    Sincroniza los juegos más populares de RAWG.
    Ejecuta diariamente (configurado en Celery Beat).
    """
    from app import create_app
    
    app = create_app()
    with app.app_context():
        try:
            game_service = GameService()
            rawg_service = game_service.rawg_service
            
            # Obtener top 100 juegos populares
            popular = rawg_service.get_popular_games(page_size=100)
            
            synced_count = 0
            failed_count = 0
            
            for game_data in popular.get('results', []):
                try:
                    game_service.import_game(str(game_data.get('id')), force_refresh=False)
                    synced_count += 1
                except Exception as e:
                    logger.error(f"Error syncing popular game {game_data.get('id')}: {e}")
                    failed_count += 1
            
            logger.info(f"Synced {synced_count} popular games, {failed_count} failed")
            return {
                'synced': synced_count,
                'failed': failed_count,
                'total': len(popular.get('results', []))
            }
            
        except Exception as e:
            logger.error(f"Error in sync_popular_games: {e}")
            raise

@shared_task
def sync_incremental():
    """
    Sincroniza solo juegos que necesitan actualización.
    Ejecuta cada 6 horas (configurado en Celery Beat).
    """
    from app import create_app
    
    app = create_app()
    with app.app_context():
        try:
            # Obtener juegos con external_id que no se han sincronizado en las últimas 24 horas
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            
            games_to_update = Videojuego.query.filter(
                Videojuego.external_id.isnot(None),
                Videojuego.api_source == 'rawg',
                db.or_(
                    Videojuego.last_synced.is_(None),
                    Videojuego.last_synced < cutoff_time
                )
            ).limit(50).all()  # Limitar a 50 por ejecución
            
            game_service = GameService()
            updated_count = 0
            failed_count = 0
            
            for game in games_to_update:
                try:
                    game_service.import_game(game.external_id, force_refresh=True)
                    updated_count += 1
                except Exception as e:
                    logger.error(f"Error updating game {game.id}: {e}")
                    failed_count += 1
            
            logger.info(f"Incremental sync: {updated_count} updated, {failed_count} failed")
            return {
                'updated': updated_count,
                'failed': failed_count,
                'total': len(games_to_update)
            }
            
        except Exception as e:
            logger.error(f"Error in sync_incremental: {e}")
            raise

