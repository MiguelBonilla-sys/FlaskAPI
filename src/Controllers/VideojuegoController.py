"""
Controlador para la gestión de videojuegos.
Maneja las peticiones HTTP y coordina con el servicio.
"""
from flask import request
from src.Services.VideojuegoService import VideojuegoService
from src.Utils import create_response, create_error_response, validate_pagination_params

class VideojuegoController:
    """
    Controlador que maneja todas las peticiones HTTP relacionadas con videojuegos.
    """
    
    @staticmethod
    def get_all():
        """
        Obtiene todos los videojuegos con filtros opcionales.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            # Obtener parámetros de consulta
            categoria = request.args.get('categoria', '').strip()
            buscar = request.args.get('buscar', '').strip()
            
            # Obtener videojuegos sin paginación
            result = VideojuegoService.get_all(
                categoria=categoria if categoria else None,
                buscar=buscar if buscar else None,
                page=1,
                per_page=1000  # Número alto para obtener todos
            )
            
            message = "Videojuegos obtenidos exitosamente"
            if categoria:
                message += f" (filtrado por categoría: {categoria})"
            if buscar:
                message += f" (búsqueda: {buscar})"
            
            return create_response(
                success=True,
                message=message,
                data=result['videojuegos'],
                count=result['total']
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener los videojuegos",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def get_by_id(videojuego_id):
        """
        Obtiene un videojuego específico por su ID.
        
        Args:
            videojuego_id (int): ID del videojuego
            
        Returns:
            tuple: (response, status_code)
        """
        try:
            videojuego = VideojuegoService.get_by_id(videojuego_id)
            
            if not videojuego:
                return create_error_response(
                    message="Videojuego no encontrado",
                    status_code=404
                )
            
            return create_response(
                success=True,
                message="Videojuego obtenido exitosamente",
                data=videojuego.to_dict()
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener el videojuego",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def create():
        """
        Crea un nuevo videojuego.
        
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
            
            # Crear videojuego
            videojuego, errors = VideojuegoService.create(data)
            
            if errors:
                return create_error_response(
                    message="Error en la validación de datos",
                    status_code=400,
                    errors=errors
                )
            
            return create_response(
                success=True,
                message="Videojuego creado exitosamente",
                data=videojuego.to_dict(),
                status_code=201
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al crear el videojuego",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def update(videojuego_id):
        """
        Actualiza un videojuego existente.
        
        Args:
            videojuego_id (int): ID del videojuego
            
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
            
            # Actualizar videojuego
            videojuego, errors = VideojuegoService.update(videojuego_id, data)
            
            if errors:
                status_code = 404 if 'no encontrado' in str(errors).lower() else 400
                return create_error_response(
                    message="Error al actualizar el videojuego",
                    status_code=status_code,
                    errors=errors
                )
            
            return create_response(
                success=True,
                message="Videojuego actualizado exitosamente",
                data=videojuego.to_dict()
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al actualizar el videojuego",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def delete(videojuego_id):
        """
        Elimina un videojuego.
        
        Args:
            videojuego_id (int): ID del videojuego
            
        Returns:
            tuple: (response, status_code)
        """
        try:
            success, errors = VideojuegoService.delete(videojuego_id)
            
            if not success:
                status_code = 404 if 'no encontrado' in str(errors).lower() else 500
                return create_error_response(
                    message="Error al eliminar el videojuego",
                    status_code=status_code,
                    errors=errors
                )
            
            return create_response(
                success=True,
                message="Videojuego eliminado exitosamente"
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al eliminar el videojuego",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def get_categories():
        """
        Obtiene todas las categorías de videojuegos.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            categories = VideojuegoService.get_categories()
            
            return create_response(
                success=True,
                message="Categorías obtenidas exitosamente",
                data=categories,
                count=len(categories)
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al obtener las categorías",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def get_statistics():
        """
        Obtiene estadísticas de los videojuegos.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            stats = VideojuegoService.get_statistics()
            
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
