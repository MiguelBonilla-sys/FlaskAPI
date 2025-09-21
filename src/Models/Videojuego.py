"""
Modelo de datos para Videojuego.
"""
from datetime import datetime
from sqlalchemy import func
from src.Config.Database import db

class Videojuego(db.Model):
    """
    Modelo de Videojuego con todas las propiedades necesarias.
    """
    __tablename__ = 'videojuegos'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    categoria = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    valoracion = db.Column(db.Numeric(3, 1), nullable=False)
    
    # Relación con desarrolladora
    desarrolladora_id = db.Column(db.Integer, db.ForeignKey('desarrolladoras.id'), nullable=True)
    
    # Campos de auditoría
    fecha_creacion = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, nombre, categoria, precio, valoracion, desarrolladora_id=None):
        """
        Constructor del modelo Videojuego.
        
        Args:
            nombre (str): Nombre del videojuego
            categoria (str): Categoría del videojuego
            precio (float): Precio del videojuego
            valoracion (float): Valoración del videojuego (0-10)
            desarrolladora_id (int, optional): ID de la desarrolladora
        """
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.valoracion = valoracion
        self.desarrolladora_id = desarrolladora_id
    
    def __repr__(self):
        """
        Representación string del objeto.
        
        Returns:
            str: Representación del videojuego
        """
        return f'<Videojuego {self.nombre}>'
    
    def to_dict(self):
        """
        Convierte el objeto a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los datos del videojuego
        """
        result = {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'precio': float(self.precio),
            'valoracion': float(self.valoracion),
            'desarrolladora_id': self.desarrolladora_id,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
        
        # Incluir información de la desarrolladora si existe
        if self.desarrolladora:
            result['desarrolladora'] = {
                'id': self.desarrolladora.id,
                'nombre': self.desarrolladora.nombre,
                'pais': self.desarrolladora.pais
            }
        
        return result
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Videojuego desde un diccionario.
        
        Args:
            data (dict): Datos del videojuego
            
        Returns:
            Videojuego: Nueva instancia de Videojuego
        """
        return cls(
            nombre=data.get('nombre'),
            categoria=data.get('categoria'),
            precio=data.get('precio'),
            valoracion=data.get('valoracion'),
            desarrolladora_id=data.get('desarrolladora_id')
        )
    
    def update_from_dict(self, data):
        """
        Actualiza los campos del videojuego desde un diccionario.
        
        Args:
            data (dict): Datos para actualizar
        """
        if 'nombre' in data:
            self.nombre = data['nombre']
        if 'categoria' in data:
            self.categoria = data['categoria']
        if 'precio' in data:
            self.precio = data['precio']
        if 'valoracion' in data:
            self.valoracion = data['valoracion']
        if 'desarrolladora_id' in data:
            self.desarrolladora_id = data['desarrolladora_id']
    
    @staticmethod
    def validate_data(data):
        """
        Valida los datos de entrada para un videojuego.
        
        Args:
            data (dict): Datos a validar
            
        Returns:
            tuple: (is_valid, errors)
        """
        errors = []
        
        # Validar nombre
        if not data.get('nombre') or not data['nombre'].strip():
            errors.append('El nombre es requerido y no puede estar vacío')
        elif len(data['nombre'].strip()) > 100:
            errors.append('El nombre no puede tener más de 100 caracteres')
        
        # Validar categoría
        if not data.get('categoria') or not data['categoria'].strip():
            errors.append('La categoría es requerida y no puede estar vacía')
        elif len(data['categoria'].strip()) > 50:
            errors.append('La categoría no puede tener más de 50 caracteres')
        
        # Validar precio
        if 'precio' not in data:
            errors.append('El precio es requerido')
        else:
            try:
                precio = float(data['precio'])
                if precio < 0:
                    errors.append('El precio debe ser mayor o igual a 0')
            except (ValueError, TypeError):
                errors.append('El precio debe ser un número válido')
        
        # Validar valoración
        if 'valoracion' not in data:
            errors.append('La valoración es requerida')
        else:
            try:
                valoracion = float(data['valoracion'])
                if valoracion < 0 or valoracion > 10:
                    errors.append('La valoración debe estar entre 0 y 10')
            except (ValueError, TypeError):
                errors.append('La valoración debe ser un número válido')
        
        return len(errors) == 0, errors
