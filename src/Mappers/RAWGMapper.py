"""
Mapper para transformar datos de RAWG API al modelo interno.
"""
from src.Utils.data_utils import safe_get


class RAWGMapper:
    """Transforma datos de RAWG API al formato del modelo interno."""
    
    @staticmethod
    def to_internal_model(rawg_data):
        """
        Transforma datos de RAWG API al modelo interno.
        
        Args:
            rawg_data: Datos de RAWG API (dict)
        
        Returns:
            dict: Datos en formato del modelo interno
        """
        return {
            'nombre': rawg_data.get('name', 'Unknown'),
            'categoria': RAWGMapper._extract_genre(rawg_data),
            'precio': 0.0,  # RAWG no tiene datos de precio directo
            'valoracion': RAWGMapper._extract_rating(rawg_data),
            'descripcion': RAWGMapper._extract_description(rawg_data),
            'imagen_url': RAWGMapper._extract_image_url(rawg_data),
            'desarrollador': RAWGMapper._extract_developer(rawg_data),
            'external_id': str(rawg_data.get('id', '')),
            'api_source': 'rawg'
        }
    
    @staticmethod
    def _extract_genre(data):
        """Extrae el primer género de la lista."""
        genres = safe_get(data, 'genres', default=[])
        if genres and len(genres) > 0:
            genre_name = safe_get(genres[0], 'name', default='Sin categoría')
            return genre_name if genre_name else 'Sin categoría'
        return 'Sin categoría'
    
    @staticmethod
    def _extract_rating(data):
        """
        Extrae y normaliza el rating.
        RAWG tiene rating 0-5 y metacritic 0-100.
        Normaliza todo a escala 0-10.
        """
        # Priorizar Metacritic si existe
        metacritic = data.get('metacritic')
        if metacritic is not None:
            # Metacritic es 0-100, normalizar a 0-10
            return float(metacritic) / 10
        
        # Si no hay Metacritic, usar rating de RAWG
        rating = data.get('rating', 0)
        if rating:
            # RAWG rating es 0-5, convertir a 0-10
            return float(rating) * 2
        
        return 0.0
    
    @staticmethod
    def _extract_developer(data):
        """Extrae el desarrollador principal."""
        developers = safe_get(data, 'developers', default=[])
        if developers and len(developers) > 0:
            developer_name = safe_get(developers[0], 'name', default='Unknown')
            return developer_name if developer_name else 'Unknown'
        return 'Unknown'
    
    @staticmethod
    def _extract_description(data):
        """Extrae la descripción del juego."""
        # RAWG tiene description_raw (texto completo) y description (HTML)
        description = data.get('description_raw') or data.get('description', '')
        if description:
            # Limpiar HTML básico si es necesario
            description = description.replace('<br>', '\n').replace('<p>', '').replace('</p>', '\n')
            # Limitar longitud
            if len(description) > 2000:
                description = description[:2000] + '...'
        return description or ''
    
    @staticmethod
    def _extract_image_url(data):
        """Extrae la URL de la imagen principal."""
        # RAWG tiene background_image como imagen principal
        image_url = data.get('background_image', '')
        return image_url or ''

