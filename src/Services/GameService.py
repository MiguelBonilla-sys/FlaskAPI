"""
Servicio orquestador que combina RAWG API con lógica de negocio local.
Implementa patrón híbrido: BD local + APIs externas.
"""
from datetime import datetime, timedelta
import time
from flask import current_app
from src.Config.Database import db
from src.Models.Videojuego import Videojuego
from src.Services.RAWGService import RAWGService
from src.Mappers.RAWGMapper import RAWGMapper
from src.Utils.exceptions import APIError, InvalidDataError
import logging


class GameService:
    """Servicio que orquesta operaciones entre BD local y APIs externas."""
    
    def __init__(self):
        """Inicializa el servicio con RAWGService."""
        self.rawg_service = RAWGService()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def import_game(self, external_id, force_refresh=False, create_sync_log=True):
        """
        Importa o actualiza un juego desde RAWG.
        
        Args:
            external_id: ID del juego en RAWG
            force_refresh: Si True, fuerza actualización aunque exista
            create_sync_log: Si True, crea un registro en SyncLog (default: True)
        
        Returns:
            Videojuego: Juego importado o actualizado
        
        Raises:
            APIError: Si falla la API externa
            InvalidDataError: Si los datos son inválidos
        """
        from src.Models.SyncLog import SyncLog
        
        # Crear registro de sincronización si se solicita
        sync_log = None
        start_time = None
        if create_sync_log:
            sync_log = SyncLog(external_id=str(external_id), api_source='rawg', status='pending')
            db.session.add(sync_log)
            db.session.commit()
            start_time = time.time()
        
        # Verificar si ya existe
        existing = Videojuego.query.filter_by(
            external_id=str(external_id),
            api_source='rawg'
        ).first()
        
        if existing and not force_refresh:
            self.logger.info(f"Game {external_id} already exists, skipping import")
            # Si existe y no se fuerza refresh, marcar sync_log como success rápidamente
            if sync_log:
                duration = time.time() - start_time if start_time else 0
                sync_log.mark_success(videojuego_id=existing.id, duration_seconds=duration)
                db.session.commit()
            return existing
        
        # Fetch desde RAWG
        try:
            external_data = self.rawg_service.get_game_details(external_id)
        except APIError as e:
            self.logger.error(f"Error fetching from RAWG: {e}")
            # Marcar sync_log como fallido si existe
            if sync_log:
                duration = time.time() - start_time if start_time else 0
                sync_log.mark_failed(error_message=str(e), duration_seconds=duration)
                try:
                    db.session.commit()
                except:
                    pass
            raise
        
        # Transformar con mapper
        try:
            internal_data = RAWGMapper.to_internal_model(external_data)
        except Exception as e:
            self.logger.error(f"Error transforming data: {e}")
            raise InvalidDataError(f"Error transforming data: {str(e)}")
        
        # Validar datos básicos
        if not internal_data.get('nombre') or internal_data['nombre'] == 'Unknown':
            raise InvalidDataError("Invalid game data: missing or invalid name")
        
        # Crear o buscar desarrolladora
        desarrolladora_id = None
        desarrollador_nombre = internal_data.get('desarrollador')
        if desarrollador_nombre and desarrollador_nombre != 'Unknown':
            from src.Models.Desarrolladora import Desarrolladora
            from src.Services.DesarrolladoraService import DesarrolladoraService
            
            # Buscar desarrolladora existente
            desarrolladora = Desarrolladora.query.filter_by(
                nombre=desarrollador_nombre
            ).first()
            
            if not desarrolladora:
                # Crear nueva desarrolladora
                # Intentar obtener más datos de RAWG si están disponibles
                developers_data = external_data.get('developers', [])
                developer_data = developers_data[0] if developers_data else {}
                
                desarrolladora_data = {
                    'nombre': desarrollador_nombre,
                    'pais': None,
                    'fundacion': None,
                    'sitio_web': None,
                    'descripcion': None
                }
                
                # Intentar obtener país si está disponible
                # RAWG no siempre tiene esta info en developers, pero lo intentamos
                
                desarrolladora, errors = DesarrolladoraService.create(desarrolladora_data)
                if desarrolladora:
                    self.logger.info(f"Created new developer: {desarrollador_nombre}")
                else:
                    self.logger.warning(f"Could not create developer: {errors}")
            
            if desarrolladora:
                desarrolladora_id = desarrolladora.id
        
        # Asignar desarrolladora_id al juego
        internal_data['desarrolladora_id'] = desarrolladora_id
        
        # Crear o actualizar en BD
        if existing:
            existing.update_from_dict(internal_data)
            existing.last_synced = datetime.utcnow()
            game = existing
        else:
            # Verificar si existe juego con mismo nombre
            nombre_existente = Videojuego.query.filter_by(
                nombre=internal_data['nombre']
            ).first()
            
            if nombre_existente:
                # Actualizar el existente con datos externos
                nombre_existente.update_from_dict(internal_data)
                nombre_existente.external_id = str(external_id)
                nombre_existente.api_source = 'rawg'
                nombre_existente.last_synced = datetime.utcnow()
                game = nombre_existente
            else:
                game = Videojuego.from_dict(internal_data)
                game.last_synced = datetime.utcnow()
                db.session.add(game)
        
        try:
            db.session.commit()
            self.logger.info(f"Game {external_id} imported/updated successfully")
            
            # Marcar sync_log como exitoso si existe
            if sync_log:
                duration = time.time() - start_time if start_time else 0
                sync_log.mark_success(videojuego_id=game.id, duration_seconds=duration)
                db.session.commit()
            
            return game
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error saving game to DB: {e}")
            
            # Marcar sync_log como fallido si existe
            if sync_log:
                duration = time.time() - start_time if start_time else 0
                sync_log.mark_failed(error_message=str(e), duration_seconds=duration)
                try:
                    db.session.commit()
                except:
                    pass  # Si falla el commit del log, continuar con el error original
            
            raise InvalidDataError(f"Error saving game: {str(e)}")
    
    def get_game(self, game_id, force_refresh=False):
        """
        Obtiene un juego, verificando BD local primero.
        
        Args:
            game_id: ID del juego en BD local
            force_refresh: Si True, refresca desde API externa
        
        Returns:
            Videojuego: Juego encontrado
        """
        game = Videojuego.query.get(game_id)
        if not game:
            return None
        
        # Si tiene external_id y necesita refresh
        if game.external_id and (force_refresh or not self._is_fresh(game)):
            try:
                return self.import_game(game.external_id, force_refresh=True)
            except APIError:
                # Si falla API, retornar datos locales aunque viejos
                self.logger.warning(f"API failed for game {game_id}, returning stale data")
                return game
        
        return game
    
    def search_hybrid(self, query, include_external=True, limit_local=10, limit_external=5):
        """
        Búsqueda híbrida: local + RAWG.
        
        Args:
            query: Término de búsqueda
            include_external: Si incluir resultados de RAWG
            limit_local: Límite de resultados locales
            limit_external: Límite de resultados externos
        
        Returns:
            dict: Resultados locales y externos
        """
        from sqlalchemy import or_
        from src.Models.Desarrolladora import Desarrolladora
        
        # Búsqueda local
        search_term = f'%{query}%'
        local_query = Videojuego.query.outerjoin(Desarrolladora).filter(
            or_(
                Videojuego.nombre.ilike(search_term),
                Videojuego.categoria.ilike(search_term),
                Desarrolladora.nombre.ilike(search_term)
            )
        ).limit(limit_local)
        
        local_results = [game.to_dict() for game in local_query.all()]
        
        result = {
            'local': local_results,
            'external': []
        }
        
        # Búsqueda externa opcional
        if include_external:
            try:
                external_data = self.rawg_service.search_games(query, page_size=limit_external)
                external_results = []
                
                for game_data in external_data.get('results', []):
                    external_results.append({
                        'nombre': game_data.get('name', 'Unknown'),
                        'categoria': RAWGMapper._extract_genre(game_data),
                        'external_id': str(game_data.get('id', '')),
                        'api_source': 'rawg',
                        'imagen_url': game_data.get('background_image', ''),
                        'valoracion': RAWGMapper._extract_rating(game_data),
                        'puede_importar': True
                    })
                
                result['external'] = external_results
            except APIError as e:
                self.logger.warning(f"Error in external search: {e}")
                # Continuar sin resultados externos
        
        return result
    
    def enrich_game(self, game_id):
        """
        Enriquece un juego local con datos adicionales de RAWG.
        
        Args:
            game_id: ID del juego en BD local
        
        Returns:
            dict: Datos enriquecidos
        """
        game = Videojuego.query.get(game_id)
        if not game:
            return None
        
        base_data = game.to_dict()
        
        # Si tiene external_id, obtener datos adicionales
        if game.external_id and game.api_source == 'rawg':
            try:
                external_data = self.rawg_service.get_game_details(game.external_id)
                
                # Agregar screenshots
                screenshots_data = self.rawg_service.get_game_screenshots(game.external_id)
                base_data['screenshots'] = [
                    s.get('image', '') for s in screenshots_data.get('results', [])[:5]
                ]
                
                # Agregar plataformas
                base_data['plataformas'] = [
                    p.get('platform', {}).get('name', '') 
                    for p in external_data.get('platforms', [])
                ]
                
                # Agregar tags
                base_data['tags'] = [
                    t.get('name', '') for t in external_data.get('tags', [])[:10]
                ]
                
                # Agregar fecha de lanzamiento
                base_data['fecha_lanzamiento'] = external_data.get('released', '')
                
            except APIError as e:
                self.logger.warning(f"Error enriching game {game_id}: {e}")
                # Continuar sin datos adicionales
        
        return base_data
    
    def _is_fresh(self, game, max_age_hours=24):
        """
        Verifica si los datos del juego están frescos.
        
        Args:
            game: Instancia de Videojuego
            max_age_hours: Edad máxima en horas
        
        Returns:
            bool: True si los datos están frescos
        """
        if not game.last_synced:
            return False
        
        age = datetime.utcnow() - game.last_synced
        return age < timedelta(hours=max_age_hours)

