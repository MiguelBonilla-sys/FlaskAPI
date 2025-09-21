"""
Modelo de datos para Desarrolladora.
"""
from datetime import datetime
from src.Config.Database import db

class Desarrolladora(db.Model):
    """
    Modelo de Desarrolladora con todas las propiedades necesarias.
    """
    __tablename__ = 'desarrolladoras'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    pais = db.Column(db.String(100), nullable=True)
    fundacion = db.Column(db.Integer, nullable=True)  # Formato YYYYMMDD
    sitio_web = db.Column(db.String(200), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    
    # Campos de auditoría
    fecha_creacion = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con videojuegos
    videojuegos = db.relationship('Videojuego', backref='desarrolladora', lazy=True)
    
    def __init__(self, nombre, pais=None, fundacion=None, sitio_web=None, descripcion=None):
        """
        Constructor del modelo Desarrolladora.
        
        Args:
            nombre (str): Nombre de la desarrolladora
            pais (str, optional): País de origen
            fundacion (int, optional): Fecha de fundación en formato YYYYMMDD
            sitio_web (str, optional): Sitio web oficial
            descripcion (str, optional): Descripción de la desarrolladora
        """
        self.nombre = nombre
        self.pais = pais
        self.fundacion = fundacion
        self.sitio_web = sitio_web
        self.descripcion = descripcion
    
    def __repr__(self):
        """
        Representación string del objeto.
        
        Returns:
            str: Representación de la desarrolladora
        """
        return f'<Desarrolladora {self.nombre}>'
    
    def to_dict(self):
        """
        Convierte el objeto a diccionario para serialización JSON.
        
        Returns:
            dict: Diccionario con los datos de la desarrolladora
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'pais': self.pais,
            'fundacion': self.fundacion,  # Ya es un entero en formato YYYYMMDD
            'sitio_web': self.sitio_web,
            'descripcion': self.descripcion,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea una instancia de Desarrolladora desde un diccionario.
        
        Args:
            data (dict): Datos de la desarrolladora
            
        Returns:
            Desarrolladora: Nueva instancia de Desarrolladora
        """
        from datetime import datetime
        
        # Convertir string de fecha a objeto date si se proporciona
        fundacion = None
        if data.get('fundacion'):
            try:
                fundacion_str = data['fundacion']
                if isinstance(fundacion_str, str):
                    fundacion = datetime.strptime(fundacion_str, '%Y-%m-%d').date()
                else:
                    fundacion = fundacion_str
            except ValueError:
                pass  # Si no se puede convertir, se mantiene None
        
        return cls(
            nombre=data.get('nombre'),
            pais=data.get('pais'),
            fundacion=fundacion,
            sitio_web=data.get('sitio_web'),
            descripcion=data.get('descripcion')
        )
    
    def update_from_dict(self, data):
        """
        Actualiza los campos de la desarrolladora desde un diccionario.
        
        Args:
            data (dict): Datos para actualizar
        """
        from datetime import datetime
        
        if 'nombre' in data:
            self.nombre = data['nombre']
        if 'pais' in data:
            self.pais = data['pais']
        if 'fundacion' in data:
            if data['fundacion']:
                try:
                    fundacion_str = data['fundacion']
                    if isinstance(fundacion_str, str):
                        self.fundacion = datetime.strptime(fundacion_str, '%Y-%m-%d').date()
                    else:
                        self.fundacion = fundacion_str
                except ValueError:
                    pass  # Si no se puede convertir, se mantiene el valor actual
            else:
                self.fundacion = None
        if 'sitio_web' in data:
            self.sitio_web = data['sitio_web']
        if 'descripcion' in data:
            self.descripcion = data['descripcion']
    
    @staticmethod
    def validate_data(data):
        """
        Valida los datos de entrada para una desarrolladora.
        
        Args:
            data (dict): Datos a validar
            
        Returns:
            tuple: (is_valid, errors)
        """
        errors = []
        
        # Validar nombre (campo obligatorio)
        if not data.get('nombre') or not data['nombre'].strip():
            errors.append('El nombre es requerido y no puede estar vacío')
        elif len(data['nombre'].strip()) > 100:
            errors.append('El nombre no puede tener más de 100 caracteres')
        
        # Validar país (opcional)
        if data.get('pais') and len(data['pais']) > 100:
            errors.append('El país no puede tener más de 100 caracteres')
        
        # Validar sitio web (opcional)
        if data.get('sitio_web') and len(data['sitio_web']) > 200:
            errors.append('El sitio web no puede tener más de 200 caracteres')
        
        # Validar fecha de fundación (opcional)
        if data.get('fundacion'):
            try:
                from datetime import datetime
                if isinstance(data['fundacion'], str):
                    datetime.strptime(data['fundacion'], '%Y-%m-%d')
            except ValueError:
                errors.append('La fecha de fundación debe tener el formato YYYY-MM-DD')
        
        return len(errors) == 0, errors