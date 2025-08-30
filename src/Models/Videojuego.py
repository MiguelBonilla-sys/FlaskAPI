from datetime import datetime
from typing import Dict, Any, Optional

class Videojuego:
    def __init__(self, id: int, nombre: str, categoria: str, precio: float, valoracion: float):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.valoracion = valoracion
        self.fecha_creacion = datetime.now()
        self.fecha_actualizacion = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el objeto a un diccionario para JSON"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'precio': self.precio,
            'valoracion': self.valoracion,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_actualizacion': self.fecha_actualizacion.isoformat()
        }
    
    def update(self, data: Dict[str, Any]) -> None:
        """Actualiza los campos del videojuego"""
        if 'nombre' in data:
            self.nombre = data['nombre']
        if 'categoria' in data:
            self.categoria = data['categoria']
        if 'precio' in data:
            self.precio = data['precio']
        if 'valoracion' in data:
            self.valoracion = data['valoracion']
        
        self.fecha_actualizacion = datetime.now()
    
    @staticmethod
    def validate_data(data: Dict[str, Any]) -> Optional[str]:
        """Valida los datos del videojuego"""
        required_fields = ['nombre', 'categoria', 'precio', 'valoracion']
        
        for field in required_fields:
            if field not in data:
                return f"El campo '{field}' es requerido"
        
        if not isinstance(data['nombre'], str) or len(data['nombre'].strip()) == 0:
            return "El nombre debe ser una cadena no vacía"
        
        if not isinstance(data['categoria'], str) or len(data['categoria'].strip()) == 0:
            return "La categoría debe ser una cadena no vacía"
        
        try:
            precio = float(data['precio'])
            if precio < 0:
                return "El precio debe ser mayor o igual a 0"
        except (ValueError, TypeError):
            return "El precio debe ser un número válido"
        
        try:
            valoracion = float(data['valoracion'])
            if not (0 <= valoracion <= 10):
                return "La valoración debe estar entre 0 y 10"
        except (ValueError, TypeError):
            return "La valoración debe ser un número válido"
        
        return None
