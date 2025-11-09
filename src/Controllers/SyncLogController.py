"""
Controlador para gestionar logs de sincronización.
"""
from flask import request
from src.Models.SyncLog import SyncLog
from src.Utils import create_response, create_error_response, validate_pagination_params


class SyncLogController:
    """Controlador para operaciones con SyncLog."""
    
    @staticmethod
    def get_all():
        """
        Obtiene todos los logs de sincronización con paginación.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            # Validar parámetros de paginación
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            # Validar valores
            if page < 1:
                page = 1
            if per_page < 1:
                per_page = 10
            if per_page > 100:
                per_page = 100
            
            # Filtros opcionales
            api_source = request.args.get('api_source', '').strip() or None
            status = request.args.get('status', '').strip() or None
            
            # Construir query
            query = SyncLog.query
            
            if api_source:
                query = query.filter_by(api_source=api_source)
            if status:
                query = query.filter_by(status=status)
            
            # Ordenar por fecha de creación (más recientes primero)
            # Usar started_at si created_at no está disponible
            try:
                query = query.order_by(SyncLog.created_at.desc())
            except:
                query = query.order_by(SyncLog.started_at.desc())
            
            # Paginación
            pagination = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            # Convertir a diccionarios
            logs = [log.to_dict() for log in pagination.items]
            
            response_data = {
                'logs': logs,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': pagination.total,
                    'total_pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
            
            return create_response(
                success=True,
                message="Logs de sincronización obtenidos exitosamente",
                data=response_data,
                count=pagination.total
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener logs de sincronización",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def get_by_id(sync_log_id):
        """
        Obtiene un log de sincronización por ID.
        
        Args:
            sync_log_id: ID del log
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            sync_log = SyncLog.query.get(sync_log_id)
            
            if not sync_log:
                return create_error_response(
                    message="Log de sincronización no encontrado",
                    status_code=404
                )
            
            return create_response(
                success=True,
                message="Log de sincronización obtenido exitosamente",
                data=sync_log.to_dict()
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener log de sincronización",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def get_recent():
        """
        Obtiene los logs de sincronización más recientes.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            limit = request.args.get('limit', 50, type=int)
            api_source = request.args.get('api_source', '').strip() or None
            
            if limit < 1 or limit > 100:
                limit = 50
            
            logs = SyncLog.get_recent_syncs(limit=limit, api_source=api_source)
            logs_data = [log.to_dict() for log in logs]
            
            return create_response(
                success=True,
                message="Logs recientes obtenidos exitosamente",
                data=logs_data,
                count=len(logs_data)
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener logs recientes",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def get_statistics():
        """
        Obtiene estadísticas de sincronizaciones.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            days = request.args.get('days', 7, type=int)
            api_source = request.args.get('api_source', '').strip() or None
            
            if days < 1 or days > 365:
                days = 7
            
            stats = SyncLog.get_stats(api_source=api_source, days=days)
            
            return create_response(
                success=True,
                message="Estadísticas obtenidas exitosamente",
                data=stats
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener estadísticas",
                status_code=500,
                errors=[str(e)]
            )

