"""
Servicio para la gestión de desarrolladoras.
Contiene toda la lógica de negocio.
"""
from sqlalchemy import or_
from src.Config.Database import db
from src.Models.Desarrolladora import Desarrolladora

class DesarrolladoraService:
    """
    Servicio que maneja todas las operaciones de negocio para desarrolladoras.
    """
    
    @staticmethod
    def get_all(buscar=None, pais=None, page=1, per_page=10):
        """
        Obtiene todas las desarrolladoras con filtros opcionales.
        
        Args:
            buscar (str): Búsqueda en nombre, país y descripción
            pais (str): Filtro por país
            page (int): Número de página para paginación
            per_page (int): Elementos por página
            
        Returns:
            dict: Resultados paginados
        """
        query = Desarrolladora.query
        
        # Aplicar filtros
        if pais:
            query = query.filter(Desarrolladora.pais.ilike(f'%{pais}%'))
            
        if buscar:
            search_term = f'%{buscar}%'
            query = query.filter(
                or_(
                    Desarrolladora.nombre.ilike(search_term),
                    Desarrolladora.pais.ilike(search_term),
                    Desarrolladora.descripcion.ilike(search_term)
                )
            )
        
        # Ordenar por fecha de creación (más recientes primero)
        query = query.order_by(Desarrolladora.fecha_creacion.desc())
        
        # Paginación
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'desarrolladoras': [desarrolladora.to_dict() for desarrolladora in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    
    @staticmethod
    def get_by_id(desarrolladora_id):
        """
        Obtiene una desarrolladora por su ID.
        
        Args:
            desarrolladora_id (int): ID de la desarrolladora
            
        Returns:
            Desarrolladora or None: La desarrolladora encontrada o None
        """
        return Desarrolladora.query.get(desarrolladora_id)
    
    @staticmethod
    def create(data):
        """
        Crea una nueva desarrolladora.
        
        Args:
            data (dict): Datos de la desarrolladora
            
        Returns:
            tuple: (desarrolladora, errors)
        """
        # Validar datos
        is_valid, errors = Desarrolladora.validate_data(data)
        if not is_valid:
            return None, errors
        
        # Verificar si ya existe una desarrolladora con el mismo nombre
        existing = Desarrolladora.query.filter_by(nombre=data['nombre'].strip()).first()
        if existing:
            return None, ['Ya existe una desarrolladora con este nombre']
        
        try:
            # Crear nueva desarrolladora
            desarrolladora = Desarrolladora.from_dict(data)
            db.session.add(desarrolladora)
            db.session.commit()
            return desarrolladora, None
            
        except Exception as e:
            db.session.rollback()
            return None, [f'Error al crear la desarrolladora: {str(e)}']
    
    @staticmethod
    def update(desarrolladora_id, data):
        """
        Actualiza una desarrolladora existente.
        
        Args:
            desarrolladora_id (int): ID de la desarrolladora
            data (dict): Datos a actualizar
            
        Returns:
            tuple: (desarrolladora, errors)
        """
        desarrolladora = Desarrolladora.query.get(desarrolladora_id)
        if not desarrolladora:
            return None, ['Desarrolladora no encontrada']
        
        # Validar solo los campos que se van a actualizar
        validation_data = {}
        if 'nombre' in data:
            validation_data['nombre'] = data['nombre']
        if 'pais' in data:
            validation_data['pais'] = data['pais']
        if 'fundacion' in data:
            validation_data['fundacion'] = data['fundacion']
        if 'sitio_web' in data:
            validation_data['sitio_web'] = data['sitio_web']
        if 'descripcion' in data:
            validation_data['descripcion'] = data['descripcion']
        
        # Si no hay datos para actualizar
        if not validation_data:
            return None, ['No se proporcionaron datos para actualizar']
        
        # Validar datos si se incluyen campos requeridos
        if validation_data:
            # Para la validación, usar los valores actuales si no se proporcionan
            complete_data = {
                'nombre': validation_data.get('nombre', desarrolladora.nombre),
                'pais': validation_data.get('pais', desarrolladora.pais),
                'fundacion': validation_data.get('fundacion', desarrolladora.fundacion),
                'sitio_web': validation_data.get('sitio_web', desarrolladora.sitio_web),
                'descripcion': validation_data.get('descripcion', desarrolladora.descripcion)
            }
            
            is_valid, errors = Desarrolladora.validate_data(complete_data)
            if not is_valid:
                return None, errors
        
        # Verificar nombre único si se está actualizando
        if 'nombre' in data and data['nombre'].strip() != desarrolladora.nombre:
            existing = Desarrolladora.query.filter_by(nombre=data['nombre'].strip()).first()
            if existing:
                return None, ['Ya existe una desarrolladora con este nombre']
        
        try:
            # Actualizar desarrolladora
            desarrolladora.update_from_dict(data)
            db.session.commit()
            return desarrolladora, None
            
        except Exception as e:
            db.session.rollback()
            return None, [f'Error al actualizar la desarrolladora: {str(e)}']
    
    @staticmethod
    def delete(desarrolladora_id):
        """
        Elimina una desarrolladora.
        
        Args:
            desarrolladora_id (int): ID de la desarrolladora
            
        Returns:
            tuple: (success, errors)
        """
        desarrolladora = Desarrolladora.query.get(desarrolladora_id)
        if not desarrolladora:
            return False, ['Desarrolladora no encontrada']
        
        # Verificar si tiene videojuegos asociados
        if desarrolladora.videojuegos:
            return False, ['No se puede eliminar la desarrolladora porque tiene videojuegos asociados']
        
        try:
            db.session.delete(desarrolladora)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, [f'Error al eliminar la desarrolladora: {str(e)}']
    
    @staticmethod
    def get_paises():
        """
        Obtiene todos los países únicos de desarrolladoras.
        
        Returns:
            list: Lista de países
        """
        paises = db.session.query(Desarrolladora.pais).distinct().all()
        return [pais[0] for pais in paises if pais[0]]
    
    @staticmethod
    def get_statistics():
        """
        Obtiene estadísticas básicas de las desarrolladoras.
        
        Returns:
            dict: Estadísticas
        """
        total = Desarrolladora.query.count()
        if total == 0:
            return {
                'total_desarrolladoras': 0,
                'paises_unicos': 0,
                'con_sitio_web': 0,
                'con_descripcion': 0
            }
        
        # Estadísticas básicas
        paises_unicos = db.session.query(Desarrolladora.pais).distinct().count()
        con_sitio_web = Desarrolladora.query.filter(Desarrolladora.sitio_web.isnot(None)).filter(Desarrolladora.sitio_web != '').count()
        con_descripcion = Desarrolladora.query.filter(Desarrolladora.descripcion.isnot(None)).filter(Desarrolladora.descripcion != '').count()
        
        return {
            'total_desarrolladoras': total,
            'paises_unicos': paises_unicos,
            'con_sitio_web': con_sitio_web,
            'con_descripcion': con_descripcion
        }
    
    @staticmethod
    def get_videojuegos_by_desarrolladora(desarrolladora_id):
        """
        Obtiene todos los videojuegos de una desarrolladora específica.
        
        Args:
            desarrolladora_id (int): ID de la desarrolladora
            
        Returns:
            tuple: (videojuegos, errors)
        """
        desarrolladora = Desarrolladora.query.get(desarrolladora_id)
        if not desarrolladora:
            return None, ['Desarrolladora no encontrada']
        
        # Importar aquí para evitar importación circular
        from src.Models.Videojuego import Videojuego
        
        videojuegos = Videojuego.query.filter_by(desarrolladora_id=desarrolladora_id).order_by(Videojuego.fecha_creacion.desc()).all()
        return [videojuego.to_dict() for videojuego in videojuegos], None
    
    @staticmethod
    def get_estadisticas_desarrolladora(desarrolladora_id):
        """
        Obtiene estadísticas específicas de una desarrolladora.
        
        Args:
            desarrolladora_id (int): ID de la desarrolladora
            
        Returns:
            tuple: (estadisticas, errors)
        """
        desarrolladora = Desarrolladora.query.get(desarrolladora_id)
        if not desarrolladora:
            return None, ['Desarrolladora no encontrada']
        
        # Importar aquí para evitar importación circular
        from src.Models.Videojuego import Videojuego
        
        # Contar videojuegos
        total_videojuegos = Videojuego.query.filter_by(desarrolladora_id=desarrolladora_id).count()
        
        if total_videojuegos == 0:
            return {
                'desarrolladora': desarrolladora.to_dict(),
                'total_videojuegos': 0,
                'valoracion_promedio': 0,
                'precio_promedio': 0,
                'categorias_desarrolladas': []
            }, None
        
        # Calcular estadísticas
        videojuegos = Videojuego.query.filter_by(desarrolladora_id=desarrolladora_id).all()
        
        valoracion_promedio = sum(float(v.valoracion) for v in videojuegos) / len(videojuegos)
        precio_promedio = sum(float(v.precio) for v in videojuegos) / len(videojuegos)
        
        # Categorías únicas
        categorias = list(set(v.categoria for v in videojuegos))
        
        return {
            'desarrolladora': desarrolladora.to_dict(),
            'total_videojuegos': total_videojuegos,
            'valoracion_promedio': round(valoracion_promedio, 2),
            'precio_promedio': round(precio_promedio, 2),
            'categorias_desarrolladas': categorias
        }, None