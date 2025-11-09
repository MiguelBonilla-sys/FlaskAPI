"""
Rutas para gestión de logs de sincronización.
"""
from flask import Blueprint
from flasgger import swag_from
from src.Controllers.SyncLogController import SyncLogController

sync_logs_bp = Blueprint('sync_logs', __name__, url_prefix='/api/sync-logs')

@sync_logs_bp.route('', methods=['GET'])
def get_all_sync_logs():
    """Endpoint para obtener todos los logs de sincronización."""
    return SyncLogController.get_all()

@sync_logs_bp.route('/recent', methods=['GET'])
def get_recent_sync_logs():
    """Endpoint para obtener logs de sincronización recientes."""
    return SyncLogController.get_recent()

@sync_logs_bp.route('/statistics', methods=['GET'])
def get_sync_statistics():
    """Endpoint para obtener estadísticas de sincronizaciones."""
    return SyncLogController.get_statistics()

@sync_logs_bp.route('/<int:sync_log_id>', methods=['GET'])
def get_sync_log_by_id(sync_log_id):
    """Endpoint para obtener un log de sincronización por ID."""
    return SyncLogController.get_by_id(sync_log_id)

