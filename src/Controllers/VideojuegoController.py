"""
Controlador para la gestión de videojuegos.
Maneja las peticiones HTTP y coordina con el servicio.
"""
from flask import request, current_app
from src.Config.Database import db
from src.Services.VideojuegoService import VideojuegoService
from src.Services.GameService import GameService
from src.Utils import create_response, create_error_response, validate_pagination_params
from src.Utils.exceptions import APIError, InvalidDataError

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
    
    @staticmethod
    def importar_externa():
        """
        Importa un videojuego desde RAWG API.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            data = request.get_json()
            
            if not data:
                return create_error_response(
                    message="No se proporcionaron datos",
                    status_code=400
                )
            
            external_id = data.get('external_id')
            if not external_id:
                return create_error_response(
                    message="external_id es requerido",
                    status_code=400
                )
            
            game_service = GameService()
            game = game_service.import_game(str(external_id))
            
            return create_response(
                success=True,
                message="Juego importado exitosamente",
                data=game.to_dict(),
                status_code=201
            )
            
        except (APIError, InvalidDataError) as e:
            return create_error_response(
                message=f"Error al importar juego: {str(e)}",
                status_code=503 if isinstance(e, APIError) else 400
            )
        except Exception as e:
            current_app.logger.error(f"Error importing game: {e}")
            return create_error_response(
                message="Error interno al importar juego",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def importar_batch():
        """
        Importa videojuegos desde RAWG API.
        Si no se proporcionan juegos, importa automáticamente juegos populares.
        Parámetros de query:
        - count: Cantidad de juegos a importar (default: 6, máx: 50)
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            from src.Models.Videojuego import Videojuego
            
            data = request.get_json() or {}
            games_to_import = data.get('games', [])
            
            # Obtener cantidad desde query parameter o usar default
            count = request.args.get('count', 6, type=int)
            if count < 1:
                count = 6
            if count > 50:
                count = 50
            
            game_service = GameService()
            results = {
                'success': [],
                'failed': [],
                'skipped': []
            }
            
            # Si no se proporcionan juegos, obtener juegos populares automáticamente
            if not games_to_import:
                try:
                    # Obtener más juegos de los necesarios para tener opciones después de filtrar
                    fetch_size = min(count * 2, 40)  # RAWG limita a 40
                    popular_games = game_service.rawg_service.get_popular_games(page_size=fetch_size)
                    games_list = popular_games.get('results', [])
                    
                    # Obtener external_ids de juegos que ya existen
                    existing_external_ids = set(
                        db.session.query(Videojuego.external_id)
                        .filter(Videojuego.api_source == 'rawg')
                        .filter(Videojuego.external_id.isnot(None))
                        .all()
                    )
                    existing_external_ids = {str(eid[0]) for eid in existing_external_ids if eid[0]}
                    
                    # Filtrar juegos que ya existen y convertir a formato esperado
                    games_to_import = []
                    for game in games_list:
                        external_id = str(game.get('id', ''))
                        if external_id and external_id not in existing_external_ids:
                            games_to_import.append({'external_id': external_id})
                            if len(games_to_import) >= count:
                                break
                    
                    current_app.logger.info(f"Importando {len(games_to_import)} juegos populares (solicitados: {count}, filtrados: {len(games_list) - len(games_to_import)} ya existían)")
                    
                    if len(games_to_import) == 0:
                        return create_response(
                            success=True,
                            message=f"No se encontraron juegos nuevos para importar. Los {count} juegos más populares ya están en la base de datos.",
                            data=results,
                            count=0,
                            status_code=200
                        )
                except Exception as e:
                    current_app.logger.error(f"Error obteniendo juegos populares: {e}")
                    return create_error_response(
                        message=f"Error al obtener juegos populares: {str(e)}",
                        status_code=503
                    )
            
            # Validar límite
            if len(games_to_import) > 50:
                return create_error_response(
                    message="Máximo 50 juegos por solicitud",
                    status_code=400
                )
            
            # Procesar cada juego
            for game_data in games_to_import:
                external_id = game_data.get('external_id') if isinstance(game_data, dict) else str(game_data)
                
                if not external_id:
                    results['failed'].append({
                        'external_id': None,
                        'error': 'external_id requerido'
                    })
                    continue
                
                try:
                    # Verificar si ya existe
                    from src.Models.Videojuego import Videojuego
                    existing = Videojuego.query.filter_by(
                        external_id=str(external_id),
                        api_source='rawg'
                    ).first()
                    
                    if existing:
                        results['skipped'].append({
                            'external_id': str(external_id),
                            'reason': 'Ya existe en base de datos'
                        })
                        continue
                    
                    # Importar
                    game = game_service.import_game(str(external_id))
                    results['success'].append(game.to_dict())
                    
                except Exception as e:
                    results['failed'].append({
                        'external_id': str(external_id),
                        'error': str(e)
                    })
            
            # Determinar código de estado
            total_success = len(results['success'])
            total_failed = len(results['failed'])
            total_skipped = len(results['skipped'])
            
            if total_success > 0:
                # Al menos uno exitoso
                if total_failed > 0:
                    status_code = 207  # Multi-Status (algunos exitosos, algunos fallidos)
                else:
                    status_code = 201  # Todos exitosos o skipped
            elif total_skipped > 0 and total_failed == 0:
                # Todos skipped (ya existen) - esto es OK, no es un error
                status_code = 200
            elif total_failed > 0:
                # Todos fallidos
                status_code = 400
            else:
                # Sin resultados (no debería pasar)
                status_code = 200
            
            return create_response(
                success=len(results['failed']) == 0,
                message=f"Importación completada: {len(results['success'])} exitosos, {len(results['failed'])} fallidos, {len(results['skipped'])} omitidos",
                data=results,
                status_code=status_code
            )
            
        except Exception as e:
            current_app.logger.error(f"Error in batch import: {e}")
            return create_error_response(
                message="Error interno en importación batch",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def get_enriquecido(videojuego_id):
        """
        Obtiene un videojuego con datos enriquecidos de RAWG.
        
        Args:
            videojuego_id: ID del videojuego
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            game_service = GameService()
            enriched_data = game_service.enrich_game(videojuego_id)
            
            if not enriched_data:
                return create_error_response(
                    message="Videojuego no encontrado",
                    status_code=404
                )
            
            return create_response(
                success=True,
                message="Juego enriquecido obtenido exitosamente",
                data=enriched_data
            )
            
        except Exception as e:
            current_app.logger.error(f"Error enriching game: {e}")
            return create_error_response(
                message="Error al obtener juego enriquecido",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def buscar_hibrida():
        """
        Búsqueda híbrida: local + RAWG.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            query = request.args.get('q', '').strip()
            include_external = request.args.get('include_external', 'false').lower() == 'true'
            
            if not query:
                return create_error_response(
                    message="Parámetro 'q' requerido",
                    status_code=400
                )
            
            game_service = GameService()
            results = game_service.search_hybrid(query, include_external=include_external)
            
            return create_response(
                success=True,
                message=f"Búsqueda completada: {len(results['local'])} locales, {len(results['external'])} externos",
                data=results,
                count=len(results['local']) + len(results['external'])
            )
            
        except Exception as e:
            current_app.logger.error(f"Error in hybrid search: {e}")
            return create_error_response(
                message="Error en búsqueda híbrida",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def sync_manual():
        """
        Inicia sincronización asíncrona manual.
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            data = request.get_json()
            
            if not data:
                return create_error_response(
                    message="No se proporcionaron datos",
                    status_code=400
                )
            
            external_id = data.get('external_id')
            if not external_id:
                return create_error_response(
                    message="external_id es requerido",
                    status_code=400
                )
            
            from src.Tasks.sync_tasks import sync_game_from_api
            task = sync_game_from_api.delay(str(external_id))
            
            return create_response(
                success=True,
                message="Sincronización iniciada",
                data={
                    'task_id': task.id,
                    'status_url': f'/api/videojuegos/sync-status/{task.id}'
                },
                status_code=202
            )
            
        except Exception as e:
            current_app.logger.error(f"Error starting sync: {e}")
            return create_error_response(
                message="Error al iniciar sincronización",
                status_code=500,
                errors=[str(e)]
            )
    
    @staticmethod
    def sync_status(task_id):
        """
        Consulta el estado de una tarea de sincronización.
        
        Args:
            task_id: ID de la tarea de Celery
        
        Returns:
            tuple: (response, status_code)
        """
        try:
            from celery.result import AsyncResult
            
            task = AsyncResult(task_id)
            
            if task.state == 'PENDING':
                response = {
                    'status': 'pending',
                    'message': 'Task en cola'
                }
            elif task.state == 'STARTED':
                response = {
                    'status': 'running',
                    'message': 'Sincronización en progreso'
                }
            elif task.state == 'SUCCESS':
                response = {
                    'status': 'completed',
                    'result': task.result
                }
            elif task.state == 'FAILURE':
                response = {
                    'status': 'failed',
                    'error': str(task.info)
                }
            else:
                response = {
                    'status': task.state,
                    'message': 'Estado desconocido'
                }
            
            return create_response(
                success=task.state == 'SUCCESS',
                message=response.get('message', ''),
                data=response
            )
            
        except Exception as e:
            current_app.logger.error(f"Error checking sync status: {e}")
            return create_error_response(
                message="Error al consultar estado de sincronización",
                status_code=500,
                errors=[str(e)]
            )
