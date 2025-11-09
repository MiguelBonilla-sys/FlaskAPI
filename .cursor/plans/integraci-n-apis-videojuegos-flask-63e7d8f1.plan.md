<!-- 63e7d8f1-7335-43b1-a43c-0723c7d758dd 58b0b39e-a414-4ee5-87aa-df82e3f70569 -->
# Plan de Integración de APIs de Videojuegos en Flask

## Objetivo

Integrar API RAWG en la aplicación Flask existente, permitiendo importación manual, búsqueda híbrida (local + externa) y sincronización automática con Celery. Configuración optimizada para Railway.

## Arquitectura General

- **Capa de Services**: Lógica de integración con RAWG API
- **Capa de Mappers**: Transformación de datos RAWG al modelo interno
- **Caché Redis**: Reducción de latencia y costos de API (Railway Redis)
- **Celery**: Sincronización asíncrona y tareas programadas (Railway workers)
- **Modelo híbrido**: Datos locales en PostgreSQL + enriquecimiento con RAWG
- **Railway-ready**: Configuración para deployment en Railway

## Cambios en el Modelo

### 1. Extender modelo Videojuego

**Archivo**: `src/Models/Videojuego.py`

- Agregar campos: `external_id`, `api_source`, `last_synced`
- Agregar campos opcionales: `descripcion`, `imagen_url`, `desarrollador` (string)
- Crear migración con Flask-Migrate

## Estructura de Directorios

### 2. Crear capa de Services para APIs externas

**Nuevos archivos**:

- `src/Services/ExternalAPIService.py` - Clase base con retry logic, circuit breaker
- `src/Services/RAWGService.py` - Integración con RAWG API
- `src/Services/SteamService.py` - Integración con Steam Web API
- `src/Services/IGDBService.py` - Integración con IGDB API
- `src/Services/GameService.py` - Orquestador que combina servicios

### 3. Crear capa de Mappers

**Nuevos archivos**:

- `src/Mappers/__init__.py`
- `src/Mappers/SteamMapper.py` - Transforma datos Steam → modelo interno
- `src/Mappers/RAWGMapper.py` - Transforma datos RAWG → modelo interno
- `src/Mappers/IGDBMapper.py` - Transforma datos IGDB → modelo interno
- `src/Utils/data_utils.py` - Helper `safe_get()` para navegación segura

### 4. Utilidades y configuración

**Nuevos archivos**:

- `src/Utils/api_client.py` - Cliente HTTP configurado con retry
- `src/Utils/cache_utils.py` - Utilidades de caché
- Actualizar `requirements.txt` con dependencias nuevas

## Dependencias a Agregar

### 5. Actualizar requirements.txt

Agregar:

- `requests` - Cliente HTTP
- `flask-caching` - Integración de caché
- `redis` - Backend de caché
- `celery` - Tareas asíncronas
- `marshmallow` - Validación y serialización (opcional, si no está)

## Implementación de Services

### 6. ExternalAPIService (Base)

**Archivo**: `src/Services/ExternalAPIService.py`

- Clase base abstracta
- Session con connection pooling
- Retry logic con backoff exponencial
- Circuit breaker pattern
- Manejo de errores (Timeout, RateLimit, HTTPError)
- Logging estructurado

### 7. RAWGService

**Archivo**: `src/Services/RAWGService.py`

- Hereda de ExternalAPIService
- Métodos: `search_games()`, `get_game_details()`, `get_popular_games()`
- Configuración de API key desde variables de entorno
- Decoradores de caché con TTL diferenciados

### 8. SteamService

**Archivo**: `src/Services/SteamService.py`

- Hereda de ExternalAPIService
- Métodos: `get_game_details()`, `get_current_price()`, `get_app_list()`
- Integración con Store API no oficial
- Manejo de precios en centavos

### 9. IGDBService

**Archivo**: `src/Services/IGDBService.py`

- Hereda de ExternalAPIService
- Autenticación OAuth con Twitch
- Métodos: `search_games()`, `get_game_details()`
- Query builder con Apicalypse

### 10. GameService (Orquestador)

**Archivo**: `src/Services/GameService.py`

- Combina servicios externos
- Patrón híbrido: BD local + APIs externas
- Método `import_game()`: fetch, transform, save
- Método `get_game()`: verifica BD, refresca si necesario
- Validación de frescura de datos

## Implementación de Mappers

### 11. Mappers para cada API

**Archivos**: `src/Mappers/*Mapper.py`

- `to_internal_model()`: transforma estructura externa → diccionario interno
- Métodos helper: `_extract_genre()`, `_extract_price()`, `_extract_rating()`
- Normalización de escalas (Metacritic 0-100 → 0-10)
- Manejo seguro de estructuras anidadas

## Endpoints de API

### 12. Nuevos endpoints en VideojuegosRoutes

**Archivo**: `src/Routes/VideojuegosRoutes.py`

- `POST /api/videojuegos/importar-externa` - Importación manual
- `POST /api/videojuegos/importar-batch` - Importación múltiple
- `GET /api/videojuegos/<id>/enriquecido` - Datos enriquecidos
- `GET /api/videojuegos/buscar` - Búsqueda híbrida (local + externa)
- `POST /api/videojuegos/sync-manual` - Iniciar sync asíncrona
- `GET /api/videojuegos/sync-status/<task_id>` - Estado de sync

### 13. Actualizar VideojuegoController

**Archivo**: `src/Controllers/VideojuegoController.py`

- Agregar métodos para nuevos endpoints
- Integración con GameService
- Manejo de errores de APIs externas

## Configuración de Caché

### 14. Configurar Flask-Caching

**Archivo**: `app.py` o `src/Config/Cache.py`

- Configuración de Redis como backend
- TTL diferenciados: juegos (24h), precios (1h), imágenes (7d)
- Decoradores `@cache.memoize()` en servicios

## Configuración de Celery (Opcional - Fase 2)

### 15. Setup de Celery

**Archivos**:

- `celery_worker.py` - Configuración de Celery
- `src/Tasks/__init__.py`
- `src/Tasks/sync_tasks.py` - Tasks de sincronización
- `docker-compose.yml` - Stack completo (opcional)

### 16. Tasks de Celery

**Archivo**: `src/Tasks/sync_tasks.py`

- `sync_game_from_api()` - Sync individual
- `sync_batch_games()` - Sync múltiple en paralelo
- `sync_popular_games()` - Sync automático diario
- `update_all_steam_prices()` - Actualización horaria de precios

## Variables de Entorno

### 17. Actualizar .env.example

Agregar:

- `RAWG_API_KEY`
- `STEAM_API_KEY`
- `TWITCH_CLIENT_ID` (para IGDB)
- `TWITCH_CLIENT_SECRET` (para IGDB)
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`

## Validación y Schemas

### 18. Actualizar VideojuegosSchema

**Archivo**: `src/Schemas/VideojuegosSchema.py`

- Agregar campos nuevos (external_id, api_source, etc.)
- Validación con Marshmallow
- Schema para importación externa

## Testing

### 19. Tests de integración

**Archivos**:

- `Test/test_external_apis.py` - Tests de servicios
- `Test/test_mappers.py` - Tests de transformación
- `Test/test_import_endpoints.py` - Tests de endpoints

## Documentación

### 20. Actualizar Swagger

**Archivo**: `src/Schemas/SwaggerSchema.py`

- Documentar nuevos endpoints
- Ejemplos de requests/responses
- Parámetros de query y body

## Orden de Implementación Recomendado

1. **Fase 1 - Base**: Modelo extendido, ExternalAPIService, RAWGService, RAWGMapper
2. **Fase 2 - Integración**: GameService, endpoints de importación, búsqueda híbrida
3. **Fase 3 - Caché**: Configurar Redis, decoradores de caché
4. **Fase 4 - Steam**: SteamService, SteamMapper, endpoints adicionales
5. **Fase 5 - IGDB**: IGDBService, IGDBMapper (opcional)
6. **Fase 6 - Async**: Celery, tasks de sincronización, docker-compose

## Consideraciones

- **Rate Limiting**: Respetar límites de cada API (RAWG: 20K/mes, Steam: 100K/día)
- **Error Handling**: Graceful degradation si API falla
- **Validación**: Validar datos transformados antes de guardar
- **Logging**: Registrar todas las interacciones con APIs externas
- **Seguridad**: API keys en variables de entorno, nunca en código

### To-dos

- [ ] Extender modelo Videojuego con campos external_id, api_source, last_synced, descripcion, imagen_url
- [ ] Crear ExternalAPIService base con retry logic, circuit breaker y manejo de errores
- [ ] Implementar RAWGService con métodos search_games, get_game_details, get_popular_games
- [ ] Crear mappers (RAWGMapper, SteamMapper, IGDBMapper) para transformar datos externos al modelo interno
- [ ] Crear GameService orquestador con patrón híbrido (BD local + APIs externas) y método import_game
- [ ] Agregar endpoints POST /importar-externa, POST /importar-batch, GET /buscar (híbrida), GET /<id>/enriquecido
- [ ] Configurar Flask-Caching con Redis y decoradores @cache.memoize en servicios con TTL diferenciados
- [ ] Implementar SteamService con métodos get_game_details, get_current_price, integración Store API
- [ ] Configurar Celery con tasks de sincronización (sync_game_from_api, sync_batch_games, sync_popular_games)
- [ ] Actualizar requirements.txt con requests, flask-caching, redis, celery, marshmallow
- [ ] Actualizar VideojuegosSchema con nuevos campos y validación para importación externa
- [ ] Documentar nuevos endpoints en Swagger con ejemplos de requests/responses