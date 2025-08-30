from typing import List, Optional, Dict, Any
from src.Models.Videojuego import Videojuego

class VideojuegoService:
    def __init__(self):
        self.videojuegos: List[Videojuego] = []
        self.next_id = 1
        self._init_sample_data()
    
    def _init_sample_data(self):
        """Inicializa algunos videojuegos de ejemplo"""
        sample_games = [
            {
                'nombre': 'The Legend of Zelda: Breath of the Wild',
                'categoria': 'Aventura',
                'precio': 59.99,
                'valoracion': 9.7
            },
            {
                'nombre': 'God of War',
                'categoria': 'Acción',
                'precio': 49.99,
                'valoracion': 9.5
            },
            {
                'nombre': 'Minecraft',
                'categoria': 'Sandbox',
                'precio': 29.99,
                'valoracion': 9.0
            },
            {
                'nombre': 'FIFA 23',
                'categoria': 'Deportes',
                'precio': 69.99,
                'valoracion': 8.2
            },
            {
                'nombre': 'Among Us',
                'categoria': 'Multijugador',
                'precio': 4.99,
                'valoracion': 8.5
            }
        ]
        
        for game_data in sample_games:
            self.create_videojuego(game_data)
    
    def get_all_videojuegos(self) -> List[Dict[str, Any]]:
        """Obtiene todos los videojuegos"""
        return [game.to_dict() for game in self.videojuegos]
    
    def get_videojuego_by_id(self, game_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un videojuego por su ID"""
        for game in self.videojuegos:
            if game.id == game_id:
                return game.to_dict()
        return None
    
    def create_videojuego(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo videojuego"""
        # Validar datos
        validation_error = Videojuego.validate_data(data)
        if validation_error:
            raise ValueError(validation_error)
        
        # Crear nuevo videojuego
        new_game = Videojuego(
            id=self.next_id,
            nombre=data['nombre'].strip(),
            categoria=data['categoria'].strip(),
            precio=float(data['precio']),
            valoracion=float(data['valoracion'])
        )
        
        self.videojuegos.append(new_game)
        self.next_id += 1
        
        return new_game.to_dict()
    
    def update_videojuego(self, game_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza un videojuego existente"""
        # Buscar el videojuego
        game = None
        for g in self.videojuegos:
            if g.id == game_id:
                game = g
                break
        
        if not game:
            return None
        
        # Validar solo los campos que se están actualizando
        update_data = {}
        for key, value in data.items():
            if key in ['nombre', 'categoria', 'precio', 'valoracion']:
                update_data[key] = value
        
        if update_data:
            validation_error = Videojuego.validate_data({
                'nombre': update_data.get('nombre', game.nombre),
                'categoria': update_data.get('categoria', game.categoria),
                'precio': update_data.get('precio', game.precio),
                'valoracion': update_data.get('valoracion', game.valoracion)
            })
            
            if validation_error:
                raise ValueError(validation_error)
            
            # Limpiar strings si existen
            if 'nombre' in update_data:
                update_data['nombre'] = update_data['nombre'].strip()
            if 'categoria' in update_data:
                update_data['categoria'] = update_data['categoria'].strip()
            
            game.update(update_data)
        
        return game.to_dict()
    
    def delete_videojuego(self, game_id: int) -> bool:
        """Elimina un videojuego"""
        for i, game in enumerate(self.videojuegos):
            if game.id == game_id:
                del self.videojuegos[i]
                return True
        return False
    
    def search_videojuegos(self, query: str) -> List[Dict[str, Any]]:
        """Busca videojuegos por nombre o categoría"""
        query_lower = query.lower()
        results = []
        
        for game in self.videojuegos:
            if (query_lower in game.nombre.lower() or 
                query_lower in game.categoria.lower()):
                results.append(game.to_dict())
        
        return results
    
    def get_videojuegos_by_categoria(self, categoria: str) -> List[Dict[str, Any]]:
        """Obtiene videojuegos por categoría"""
        categoria_lower = categoria.lower()
        results = []
        
        for game in self.videojuegos:
            if game.categoria.lower() == categoria_lower:
                results.append(game.to_dict())
        
        return results

# Instancia global del servicio
videojuego_service = VideojuegoService()
