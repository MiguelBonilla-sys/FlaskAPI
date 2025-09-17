y# Guía para Agentes de IA (FlaskAPI)

Resumen práctico para ser productivo de inmediato en esta API Flask.

## Arquitectura
- Capas: `Routes → Controllers → Services → Models`.
  - `Routes`: blueprints + `@swag_from` con esquemas en `src/Schemas/*`.
  - `Controllers`: entrada mínima y respuestas con `src/Utils.create_response|create_error_response`.
  - `Services`: lógica de negocio; acceso a DB solo vía `src.Config.Database.db`.
  - `Models`: SQLAlchemy con `to_dict()`, `from_dict()`, `validate_data()`, `update_from_dict()`.
- App factory: `app.py:create_app()` registra Swagger, DB, blueprints y middlewares.
- Producción: `src/wsgi/wsgi.py` (`application`/`app`), Gunicorn (Procfile/start.sh).

### Flujo completo
- Bootstrap: `create_app()` carga `.env`, configura `Swagger(config/template desde src/Schemas)`, inicializa DB (`init_db`), registra blueprints (`src/Routes/__init__.py`), configura middlewares (`error_handler.setup_*`).
- Request → Route (`ApiRoutes.py` / `VideojuegosRoutes.py`) → Controller (`VideojuegoController`) → Service (`VideojuegoService`) → `db`/`Model` (`Videojuego`) → vuelve con `create_response(...)`.
- Swagger UI: `GET /apidocs/` servido por Flasgger; `Schemas/__init__.py` calcula `host/schemes` con `Utils.detect_railway_host()` para despliegues Railway.
- Errores/logging/CORS: centralizado en `src/Middlewares/error_handler.py` con handlers 400/404/405/422/500, logging de requests y headers CORS.

### Middlewares
- Archivo: `src/Middlewares/error_handler.py`.
- Funciones clave registradas en `create_app()`:
  - `register_error_handlers(app)`: maneja 400/404/405/422/500 y `HTTPException/Exception` vía `Utils.create_error_response`.
  - `setup_logging(app)`: logging para producción y nivel del app logger.
  - `log_request_info(app)`: `@before_request` y `@after_request` para trazar método, ruta y status.
  - `setup_cors(app)`: agrega headers CORS estándar (Origin/Headers/Methods).
- Extensión: para nuevos errores, añade otro `@app.errorhandler(Codigo)` dentro de `register_error_handlers`.

Ejemplos rápidos (añadir dentro de `register_error_handlers` y `setup_cors`):
```python
# Error 429 personalizado
@app.errorhandler(429)
def too_many_requests(error):
  return create_error_response("Demasiadas solicitudes", 429, ["Rate limit excedido"]) 

# CORS restringido por ORIGINS en .env (coma-separado)
allowed = set(os.getenv("CORS_ORIGINS", "*").split(","))
@app.after_request
def after_request(resp):
  origin = request.headers.get('Origin', '*')
  if "*" in allowed or origin in allowed:
    resp.headers['Access-Control-Allow-Origin'] = origin if origin != None else '*'
  resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
  resp.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
  return resp
```

### Config (DB)
- Archivo: `src/Config/Database.py`.
- Objetos: `db = SQLAlchemy()`, `migrate = Migrate()`.
- `init_db(app)`: arma `SQLALCHEMY_DATABASE_URI` desde `DATABASE_URL` o `PG*`, configura engine (`pool_pre_ping`, `pool_recycle`), inicializa `db` y `migrate`.
- `create_tables()`: ejecuta `db.create_all()` (requiere app context).
- `get_db()`: retorna la instancia `db`.
- Uso: accede a la DB siempre a través de `src.Config.Database.db` en Services (no desde Routes/Controllers).

## Convenciones
- Respuestas JSON estandarizadas: usa `Utils.create_response`/`create_error_response` siempre en controladores.
- Swagger: define esquemas en `src/Schemas/*` y referencia con `@swag_from(schema_dict)`.
- Blueprints: `src/Routes/ApiRoutes.py` (health/info), `src/Routes/VideojuegosRoutes.py` (`/api/videojuegos`).
- Validación: central en `Model.validate_data`; no dupliques en controllers.
- Consultas: filtra con `ilike`/`or_` y ordena por fecha; pagina en servicios.
- Errores/log/CORS: `src/Middlewares/error_handler.py`.

## Config y Base de Datos
- Inicializa DB: `src/Config/Database.init_db(app)`; crea tablas con `db.create_all()` (en contexto de app).
- Conexión: `DATABASE_URL` o fallback con `PG*` (`PGUSER/PGPASSWORD/PGHOST/PGPORT/PGDATABASE`).
- Migraciones: `Flask-Migrate` disponible; si cambias modelos, prepara `flask db init/migrate/upgrade` (no hay CLI aún).

## Workflows
- Local (Windows CMD):
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  set FLASK_DEBUG=true
  python Test\init_db.py
  python app.py
  ```
- Endpoints útiles: `GET /api/`, `GET /apidocs/`, `GET /health`.
- Docker:
  ```cmd
  docker build -t flaskapi .
  docker run -p 5000:5000 --env-file .env flaskapi
  ```
- Railway: Gunicorn (`Procfile`/`start.sh`), host dinámico vía `Utils.detect_railway_host()`.

## Migraciones (Flask-Migrate)
- Requisitos: tener `Flask-Migrate` instalado (ya en `requirements.txt`). Define `FLASK_APP=app.py` o usa el flag `-A`.
- Inicializar y generar migraciones:
  ```cmd
  set FLASK_APP=app.py
  flask db init
  flask db migrate -m "init"
  flask db upgrade
  ```
- Cambios en modelos: tras editar `src/Models/*`, vuelve a `flask db migrate -m "<mensaje>"` y `flask db upgrade`.
- Nota: `init_db(app)` ya configura `Migrate(app, db)` a través de `src/Config/Database.py`.

## Extensiones de dominio (ejemplo)
- Pasos: Model → Service → Controller → Schemas → Route → registrar en `src/Routes/__init__.py`.
- Ejemplos:
  ```python
  # Servicio (filtro)
  if categoria: query = query.filter(Model.categoria.ilike(f"%{categoria}%"))
  if buscar: query = query.filter(or_(Model.nombre.ilike(term), Model.categoria.ilike(term)))
  # Respuesta
  return create_response(True, "OK", data=obj.to_dict())
  ```

## Notas
- `precio` y `valoracion` son `Numeric` → castear a `float` en `to_dict()`.
- `start.sh`: variables `WORKERS`/`TIMEOUT` (no necesarias en local).
- Sin tests formales; usar `Test/init_db.py` para datos de ejemplo.

¿Falta algo clave para tu flujo? Indícalo y lo añadimos.
