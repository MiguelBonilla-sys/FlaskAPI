"""
Servicio para la gestión de videojuegos.
Contiene toda la lógica de negocio.
"""
from sqlalchemy import or_
from src.Config.Database import db
from src.Models.Videojuego import Videojuego

class VideojuegoService:
    """
    Servicio que maneja todas las operaciones de negocio para videojuegos.
    """
    
    @staticmethod
    def get_all(categoria=None, buscar=None, page=1, per_page=10):
        """
        Obtiene todos los videojuegos con filtros opcionales.
        
        Args:
            categoria (str): Filtro por categoría
            buscar (str): Búsqueda en nombre y categoría
            page (int): Número de página para paginación
            per_page (int): Elementos por página
            
        Returns:
            dict: Resultados paginados
        """
        query = Videojuego.query
        
        # Aplicar filtros
        if categoria:
            query = query.filter(Videojuego.categoria.ilike(f'%{categoria}%'))
            
        if buscar:
            search_term = f'%{buscar}%'
            query = query.filter(
                or_(
                    Videojuego.nombre.ilike(search_term),
                    Videojuego.categoria.ilike(search_term)
                )
            )
        
        # Ordenar por fecha de creación (más recientes primero)
        query = query.order_by(Videojuego.fecha_creacion.desc())
        
        # Paginación
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'videojuegos': [videojuego.to_dict() for videojuego in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    
    @staticmethod
    def get_by_id(videojuego_id):
        """
        Obtiene un videojuego por su ID.
        
        Args:
            videojuego_id (int): ID del videojuego
            
        Returns:
            Videojuego or None: El videojuego encontrado o None
        """
        return Videojuego.query.get(videojuego_id)
    
    @staticmethod
    def create(data):
        """
        Crea un nuevo videojuego.
        
        Args:
            data (dict): Datos del videojuego
            
        Returns:
            tuple: (videojuego, errors)
        """
        # Validar datos
        is_valid, errors = Videojuego.validate_data(data)
        if not is_valid:
            return None, errors
        
        # Verificar si ya existe un videojuego con el mismo nombre
        existing = Videojuego.query.filter_by(nombre=data['nombre'].strip()).first()
        if existing:
            return None, ['Ya existe un videojuego con este nombre']
        
        try:
            # Crear nuevo videojuego
            videojuego = Videojuego.from_dict(data)
            db.session.add(videojuego)
            db.session.commit()
            return videojuego, None
            
        except Exception as e:
            db.session.rollback()
            return None, [f'Error al crear el videojuego: {str(e)}']
    
    @staticmethod
    def update(videojuego_id, data):
        """
        Actualiza un videojuego existente.
        
        Args:
            videojuego_id (int): ID del videojuego
            data (dict): Datos a actualizar
            
        Returns:
            tuple: (videojuego, errors)
        """
        videojuego = Videojuego.query.get(videojuego_id)
        if not videojuego:
            return None, ['Videojuego no encontrado']
        
        # Validar solo los campos que se van a actualizar
        validation_data = {}
        if 'nombre' in data:
            validation_data['nombre'] = data['nombre']
        if 'categoria' in data:
            validation_data['categoria'] = data['categoria']
        if 'precio' in data:
            validation_data['precio'] = data['precio']
        if 'valoracion' in data:
            validation_data['valoracion'] = data['valoracion']
        
        # Si no hay datos para actualizar
        if not validation_data:
            return None, ['No se proporcionaron datos para actualizar']
        
        # Validar datos si se incluyen campos requeridos
        if validation_data:
            # Para la validación, usar los valores actuales si no se proporcionan
            complete_data = {
                'nombre': validation_data.get('nombre', videojuego.nombre),
                'categoria': validation_data.get('categoria', videojuego.categoria),
                'precio': validation_data.get('precio', videojuego.precio),
                'valoracion': validation_data.get('valoracion', videojuego.valoracion)
            }
            
            is_valid, errors = Videojuego.validate_data(complete_data)
            if not is_valid:
                return None, errors
        
        # Verificar nombre único si se está actualizando
        if 'nombre' in data and data['nombre'].strip() != videojuego.nombre:
            existing = Videojuego.query.filter_by(nombre=data['nombre'].strip()).first()
            if existing:
                return None, ['Ya existe un videojuego con este nombre']
        
        try:
            # Actualizar videojuego
            videojuego.update_from_dict(data)
            db.session.commit()
            return videojuego, None
            
        except Exception as e:
            db.session.rollback()
            return None, [f'Error al actualizar el videojuego: {str(e)}']
    
    @staticmethod
    def delete(videojuego_id):
        """
        Elimina un videojuego.
        
        Args:
            videojuego_id (int): ID del videojuego
            
        Returns:
            tuple: (success, errors)
        """
        videojuego = Videojuego.query.get(videojuego_id)
        if not videojuego:
            return False, ['Videojuego no encontrado']
        
        try:
            db.session.delete(videojuego)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, [f'Error al eliminar el videojuego: {str(e)}']
    
    @staticmethod
    def get_categories():
        """
        Obtiene todas las categorías únicas de videojuegos.
        
        Returns:
            list: Lista de categorías
        """
        categories = db.session.query(Videojuego.categoria).distinct().all()
        return [cat[0] for cat in categories if cat[0]]
    
    @staticmethod
    def get_statistics():
        """
        Obtiene estadísticas básicas de los videojuegos.
        
        Returns:
            dict: Estadísticas
        """
        total = Videojuego.query.count()
        if total == 0:
            return {
                'total_videojuegos': 0,
                'categorias_unicas': 0,
                'precio_promedio': 0,
                'valoracion_promedio': 0
            }
        
        # Estadísticas básicas
        precio_promedio = db.session.query(db.func.avg(Videojuego.precio)).scalar()
        valoracion_promedio = db.session.query(db.func.avg(Videojuego.valoracion)).scalar()
        categorias_unicas = db.session.query(Videojuego.categoria).distinct().count()
        
        return {
            'total_videojuegos': total,
            'categorias_unicas': categorias_unicas,
            'precio_promedio': float(precio_promedio) if precio_promedio else 0,
            'valoracion_promedio': float(valoracion_promedio) if valoracion_promedio else 0
        }
