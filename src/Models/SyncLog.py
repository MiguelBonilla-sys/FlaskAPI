"""
Modelo de datos para SyncLog - Registro de sincronizaciones con APIs externas.
"""
from datetime import datetime
from src.Config.Database import db

class SyncLog(db.Model):
    """
    Modelo para registrar sincronizaciones de juegos desde APIs externas.
    """
    __tablename__ = 'sync_logs'
    
    # Campos principales
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    external_id = db.Column(db.String(100), nullable=False)  # ID del juego en la API externa
    api_source = db.Column(db.String(50), nullable=False, default='rawg')  # Fuente de la API
    videojuego_id = db.Column(db.Integer, db.ForeignKey('videojuegos.id'), nullable=True)  # ID del juego local
    
    # Estado de la sincronización
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, success, failed
    error_message = db.Column(db.Text, nullable=True)  # Mensaje de error si falla
    
    # Metadatos
    started_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    duration_seconds = db.Column(db.Float, nullable=True)  # Duración en segundos
    
    # Campos de auditoría
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    
    def __init__(self, external_id, api_source='rawg', videojuego_id=None, status='pending'):
        """
        Inicializa un nuevo registro de sincronización.
        
        Args:
            external_id: ID del juego en la API externa
            api_source: Fuente de la API (rawg, steam, igdb)
            videojuego_id: ID del juego en la BD local (si existe)
            status: Estado inicial (pending, success, failed)
        """
        self.external_id = external_id
        self.api_source = api_source
        self.videojuego_id = videojuego_id
        self.status = status
        self.started_at = datetime.utcnow()
    
    def mark_success(self, videojuego_id=None, duration_seconds=None):
        """
        Marca la sincronización como exitosa.
        
        Args:
            videojuego_id: ID del juego local si se creó/actualizó
            duration_seconds: Duración de la sincronización
        """
        self.status = 'success'
        self.completed_at = datetime.utcnow()
        if videojuego_id:
            self.videojuego_id = videojuego_id
        if duration_seconds:
            self.duration_seconds = duration_seconds
        else:
            # Calcular duración automáticamente
            if self.started_at and self.completed_at:
                delta = self.completed_at - self.started_at
                self.duration_seconds = delta.total_seconds()
    
    def mark_failed(self, error_message, duration_seconds=None):
        """
        Marca la sincronización como fallida.
        
        Args:
            error_message: Mensaje de error
            duration_seconds: Duración antes del fallo
        """
        self.status = 'failed'
        self.error_message = error_message
        self.completed_at = datetime.utcnow()
        if duration_seconds:
            self.duration_seconds = duration_seconds
        else:
            # Calcular duración automáticamente
            if self.started_at and self.completed_at:
                delta = self.completed_at - self.started_at
                self.duration_seconds = delta.total_seconds()
    
    def to_dict(self):
        """
        Convierte el registro a diccionario.
        
        Returns:
            dict: Datos del registro de sincronización
        """
        return {
            'id': self.id,
            'external_id': self.external_id,
            'api_source': self.api_source,
            'videojuego_id': self.videojuego_id,
            'status': self.status,
            'error_message': self.error_message,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_seconds': self.duration_seconds,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def get_recent_syncs(cls, limit=50, api_source=None):
        """
        Obtiene las sincronizaciones recientes.
        
        Args:
            limit: Número máximo de registros
            api_source: Filtrar por fuente de API (opcional)
        
        Returns:
            list: Lista de registros de sincronización
        """
        query = cls.query.order_by(cls.created_at.desc())
        
        if api_source:
            query = query.filter_by(api_source=api_source)
        
        return query.limit(limit).all()
    
    @classmethod
    def get_stats(cls, api_source=None, days=7):
        """
        Obtiene estadísticas de sincronizaciones.
        
        Args:
            api_source: Filtrar por fuente de API (opcional)
            days: Número de días a considerar
        
        Returns:
            dict: Estadísticas de sincronizaciones
        """
        from datetime import timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        query = cls.query.filter(cls.created_at >= cutoff_date)
        
        if api_source:
            query = query.filter_by(api_source=api_source)
        
        total = query.count()
        successful = query.filter_by(status='success').count()
        failed = query.filter_by(status='failed').count()
        pending = query.filter_by(status='pending').count()
        
        return {
            'total': total,
            'successful': successful,
            'failed': failed,
            'pending': pending,
            'success_rate': (successful / total * 100) if total > 0 else 0
        }

