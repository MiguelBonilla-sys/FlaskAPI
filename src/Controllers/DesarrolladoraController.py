"""
Controlador para la gestión de desarrolladoras.
Maneja las peticiones HTTP y coordina con el servicio.
"""
from flask import request
from src.Services.DesarrolladoraService import DesarrolladoraService
from src.Utils import create_response, create_error_response

class DesarrolladoraController:
    """
    Controlador que maneja todas las peticiones HTTP relacionadas con desarrolladoras.
    """
    
    @staticmethod
    def get_all():
        """
        Obtiene todas las desarrolladoras con filtros opcionales.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            # Obtener parámetros de consulta
            buscar = request.args.get('buscar', '').strip()
            pais = request.args.get('pais', '').strip()
            
            # Obtener desarrolladoras sin paginación
            result = DesarrolladoraService.get_all(
                buscar=buscar if buscar else None,
                pais=pais if pais else None,
                page=1,
                per_page=1000  # Número alto para obtener todas
            )
            
            message = "Desarrolladoras obtenidas exitosamente"
            if pais:
                message += f" (filtrado por país: {pais})"
            if buscar:
                message += f" (búsqueda: {buscar})"
            
            return create_response(
                success=True,
                message=message,
                data=result['desarrolladoras'],
                count=result['total']
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener las desarrolladoras",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def get_by_id(desarrolladora_id):
        """
        Obtiene una desarrolladora específica por su ID.
        
        Args:
            desarrolladora_id (int): ID de la desarrolladora
            
        Returns:
            tuple: (response, status_code)
        """
        try:
            desarrolladora = DesarrolladoraService.get_by_id(desarrolladora_id)
            
            if not desarrolladora:
                return create_error_response(
                    message="Desarrolladora no encontrada",
                    status_code=404
                )
            
            return create_response(
                success=True,
                message="Desarrolladora obtenida exitosamente",
                data=desarrolladora.to_dict()
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener la desarrolladora",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def create():
        """
        Crea una nueva desarrolladora.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            # Obtener datos del request
            data = request.get_json()
            
            if not data:
                return create_error_response(
                    message="No se proporcionaron datos",
                    status_code=400
                )
            
            # Crear desarrolladora
            desarrolladora, errors = DesarrolladoraService.create(data)
            
            if errors:
                return create_error_response(
                    message="Error al crear la desarrolladora",
                    status_code=400,
                    errors=errors
                )
            
            return create_response(
                success=True,
                message="Desarrolladora creada exitosamente",
                data=desarrolladora.to_dict(),
                status_code=201
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al crear la desarrolladora",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def update(desarrolladora_id):
        """
        Actualiza una desarrolladora existente.
        
        Args:
            desarrolladora_id (int): ID de la desarrolladora
            
        Returns:
            tuple: (response, status_code)
        """
        try:
            # Obtener datos del request
            data = request.get_json()
            
            if not data:
                return create_error_response(
                    message="No se proporcionaron datos para actualizar",
                    status_code=400
                )
            
            # Actualizar desarrolladora
            desarrolladora, errors = DesarrolladoraService.update(desarrolladora_id, data)
            
            if errors:
                status_code = 404 if "no encontrada" in errors[0] else 400
                return create_error_response(
                    message="Error al actualizar la desarrolladora",
                    status_code=status_code,
                    errors=errors
                )
            
            return create_response(
                success=True,
                message="Desarrolladora actualizada exitosamente",
                data=desarrolladora.to_dict()
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al actualizar la desarrolladora",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def delete(desarrolladora_id):
        """
        Elimina una desarrolladora.
        
        Args:
            desarrolladora_id (int): ID de la desarrolladora
            
        Returns:
            tuple: (response, status_code)
        """
        try:
            # Eliminar desarrolladora
            success, errors = DesarrolladoraService.delete(desarrolladora_id)
            
            if not success:
                status_code = 404 if "no encontrada" in errors[0] else 400
                return create_error_response(
                    message="Error al eliminar la desarrolladora",
                    status_code=status_code,
                    errors=errors
                )
            
            return create_response(
                success=True,
                message="Desarrolladora eliminada exitosamente"
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al eliminar la desarrolladora",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def get_paises():
        """
        Obtiene todos los países únicos de desarrolladoras.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            paises = DesarrolladoraService.get_paises()
            
            return create_response(
                success=True,
                message="Países obtenidos exitosamente",
                data=paises,
                count=len(paises)
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener los países",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def get_statistics():
        """
        Obtiene estadísticas básicas de desarrolladoras.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            stats = DesarrolladoraService.get_statistics()
            
            return create_response(
                success=True,
                message="Estadísticas obtenidas exitosamente",
                data=stats
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener las estadísticas",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def get_videojuegos(desarrolladora_id):
        """
        Obtiene todos los videojuegos de una desarrolladora específica.
        
        Args:
            desarrolladora_id (int): ID de la desarrolladora
            
        Returns:
            tuple: (response, status_code)
        """
        try:
            videojuegos, errors = DesarrolladoraService.get_videojuegos_by_desarrolladora(desarrolladora_id)
            
            if errors:
                return create_error_response(
                    message="Error al obtener los videojuegos de la desarrolladora",
                    status_code=404,
                    errors=errors
                )
            
            return create_response(
                success=True,
                message="Videojuegos de la desarrolladora obtenidos exitosamente",
                data=videojuegos,
                count=len(videojuegos)
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener los videojuegos de la desarrolladora",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def get_estadisticas_desarrolladora(desarrolladora_id):
        """
        Obtiene estadísticas específicas de una desarrolladora.
        
        Args:
            desarrolladora_id (int): ID de la desarrolladora
            
        Returns:
            tuple: (response, status_code)
        """
        try:
            estadisticas, errors = DesarrolladoraService.get_estadisticas_desarrolladora(desarrolladora_id)
            
            if errors:
                return create_error_response(
                    message="Error al obtener las estadísticas de la desarrolladora",
                    status_code=404,
                    errors=errors
                )
            
            return create_response(
                success=True,
                message="Estadísticas de la desarrolladora obtenidas exitosamente",
                data=estadisticas
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener las estadísticas de la desarrolladora",
                status_code=500,
                errors=[str(e)]
            )