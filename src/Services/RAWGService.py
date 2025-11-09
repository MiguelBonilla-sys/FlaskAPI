"""
Servicio para integración con RAWG API.
"""
import os
from flask import current_app
from src.Services.ExternalAPIService import ExternalAPIService
from src.Utils.exceptions import APIError
from src.Config.Cache import cache


class RAWGService(ExternalAPIService):
    """Servicio para interactuar con RAWG API."""
    
    BASE_URL = "https://api.rawg.io/api"
    
    def __init__(self):
        """Inicializa el servicio con API key."""
        super().__init__()
        # Obtener API key desde configuración
        self.api_key = os.getenv('RAWG_API_KEY') or current_app.config.get('RAWG_API_KEY')
        if not self.api_key:
            self.logger.warning("RAWG_API_KEY no configurada")
    
    def _get_base_params(self):
        """Retorna parámetros base para todas las peticiones."""
        return {'key': self.api_key} if self.api_key else {}
    
    @cache.memoize(timeout=1800)  # 30 minutos
    def search_games(self, query, page_size=10, page=1):
        """
        Busca juegos en RAWG (con caché de 30min).
        
        Args:
            query: Término de búsqueda
            page_size: Número de resultados por página (máx 40)
            page: Número de página
        
        Returns:
            dict: Resultados de la búsqueda
        """
        url = f"{self.BASE_URL}/games"
        params = {
            **self._get_base_params(),
            'search': query,
            'page_size': min(page_size, 40),  # RAWG limita a 40
            'page': page
        }
        
        try:
            return self._make_request(url, params=params)
        except Exception as e:
            self.logger.error(f"Error searching games: {e}")
            raise APIError(f"Error searching games in RAWG: {str(e)}")
    
    @cache.memoize(timeout=86400)  # 24 horas
    def get_game_details(self, game_id):
        """
        Obtiene detalles completos de un juego (con caché de 24h).
        
        Args:
            game_id: ID del juego en RAWG
        
        Returns:
            dict: Detalles del juego
        """
        url = f"{self.BASE_URL}/games/{game_id}"
        params = self._get_base_params()
        
        try:
            return self._make_request(url, params=params)
        except Exception as e:
            self.logger.error(f"Error getting game details for {game_id}: {e}")
            raise APIError(f"Error getting game details from RAWG: {str(e)}")
    
    def get_popular_games(self, page_size=100):
        """
        Obtiene juegos populares ordenados por rating.
        
        Args:
            page_size: Número de resultados (máx 40)
        
        Returns:
            dict: Lista de juegos populares
        """
        url = f"{self.BASE_URL}/games"
        params = {
            **self._get_base_params(),
            'ordering': '-rating',  # Ordenar por rating descendente
            'page_size': min(page_size, 40),
            'page': 1
        }
        
        try:
            return self._make_request(url, params=params)
        except Exception as e:
            self.logger.error(f"Error getting popular games: {e}")
            raise APIError(f"Error getting popular games from RAWG: {str(e)}")
    
    @cache.memoize(timeout=604800)  # 7 días
    def get_game_screenshots(self, game_id):
        """
        Obtiene screenshots de un juego (con caché de 7 días).
        
        Args:
            game_id: ID del juego en RAWG
        
        Returns:
            dict: Lista de screenshots
        """
        url = f"{self.BASE_URL}/games/{game_id}/screenshots"
        params = self._get_base_params()
        
        try:
            return self._make_request(url, params=params)
        except Exception as e:
            self.logger.error(f"Error getting screenshots for {game_id}: {e}")
            raise APIError(f"Error getting screenshots from RAWG: {str(e)}")

