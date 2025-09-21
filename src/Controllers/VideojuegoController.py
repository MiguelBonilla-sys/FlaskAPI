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
            desarrolladora_id = request.args.get('desarrolladora_id', '').strip()
            
            # Convertir desarrolladora_id a entero si se proporciona
            desarrolladora_id_int = None
            if desarrolladora_id:
                try:
                    desarrolladora_id_int = int(desarrolladora_id)
                except ValueError:
                    return create_error_response(
                        message="El ID de desarrolladora debe ser un número entero",
                        status_code=400
                    )
            
            # Obtener videojuegos sin paginación
            result = VideojuegoService.get_all(
                categoria=categoria if categoria else None,
                buscar=buscar if buscar else None,
                desarrolladora_id=desarrolladora_id_int,
                page=1,
                per_page=1000  # Número alto para obtener todos
            )
            
            message = "Videojuegos obtenidos exitosamente"
            if categoria:
                message += f" (filtrado por categoría: {categoria})"
            if desarrolladora_id_int:
                message += f" (filtrado por desarrolladora ID: {desarrolladora_id_int})"
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
    
    @staticmethod
    def busqueda_avanzada():
        """
        Realiza una búsqueda avanzada con múltiples filtros.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            # Obtener parámetros de consulta
            categoria = request.args.get('categoria', '').strip() or None
            buscar = request.args.get('buscar', '').strip() or None
            
            # Parámetros numéricos
            precio_min = request.args.get('precio_min')
            precio_max = request.args.get('precio_max')
            valoracion_min = request.args.get('valoracion_min')
            desarrolladora_id = request.args.get('desarrolladora_id')
            
            # Convertir parámetros numéricos
            try:
                precio_min = float(precio_min) if precio_min else None
                precio_max = float(precio_max) if precio_max else None
                valoracion_min = float(valoracion_min) if valoracion_min else None
                desarrolladora_id = int(desarrolladora_id) if desarrolladora_id else None
            except ValueError as ve:
                return create_error_response(
                    message="Parámetros numéricos inválidos",
                    status_code=400,
                    errors=[f"Error en conversión de números: {str(ve)}"]
                )
            
            # Validaciones
            if precio_min is not None and precio_min < 0:
                return create_error_response(
                    message="El precio mínimo debe ser mayor o igual a 0",
                    status_code=400
                )
                
            if precio_max is not None and precio_max < 0:
                return create_error_response(
                    message="El precio máximo debe ser mayor o igual a 0",
                    status_code=400
                )
                
            if precio_min is not None and precio_max is not None and precio_min > precio_max:
                return create_error_response(
                    message="El precio mínimo no puede ser mayor al precio máximo",
                    status_code=400
                )
                
            if valoracion_min is not None and (valoracion_min < 0 or valoracion_min > 10):
                return create_error_response(
                    message="La valoración mínima debe estar entre 0 y 10",
                    status_code=400
                )
            
            # Realizar búsqueda
            result = VideojuegoService.busqueda_avanzada(
                categoria=categoria,
                precio_min=precio_min,
                precio_max=precio_max,
                valoracion_min=valoracion_min,
                desarrolladora_id=desarrolladora_id,
                buscar=buscar,
                page=1,
                per_page=1000
            )
            
            # Construir mensaje descriptivo
            filtros_activos = []
            if categoria:
                filtros_activos.append(f"categoría: {categoria}")
            if precio_min is not None:
                filtros_activos.append(f"precio mín: ${precio_min}")
            if precio_max is not None:
                filtros_activos.append(f"precio máx: ${precio_max}")
            if valoracion_min is not None:
                filtros_activos.append(f"valoración mín: {valoracion_min}")
            if desarrolladora_id:
                filtros_activos.append(f"desarrolladora ID: {desarrolladora_id}")
            if buscar:
                filtros_activos.append(f"búsqueda: {buscar}")
            
            message = "Búsqueda avanzada realizada exitosamente"
            if filtros_activos:
                message += f" con filtros: {', '.join(filtros_activos)}"
            
            return create_response(
                success=True,
                message=message,
                data=result['videojuegos'],
                count=result['total']
            )
            
        except Exception as e:
            return create_error_response(
                message="Error al realizar la búsqueda avanzada",
                status_code=500,
                errors=[str(e)]
            )
