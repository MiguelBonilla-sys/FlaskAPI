# Guía de Tests

Esta guía explica cómo ejecutar y entender los tests del proyecto.

## Estructura de Tests

```
Test/
├── conftest.py                    # Configuración compartida de pytest
├── pytest.ini                     # Configuración de pytest
├── test_videojuegos_endpoints.py  # Tests de endpoints básicos
├── test_rawg_integration.py       # Tests de integración RAWG API
├── test_services.py               # Tests unitarios de servicios
├── test_create_videojuego.py     # Test rápido de creación
├── ejemplo_crear_con_desarrolladora.py  # Ejemplo de uso
└── init_db.py                    # Script de inicialización de BD
```

## Tipos de Tests

### 1. Tests de Integración (`test_rawg_integration.py`)

Tests que verifican la integración completa con RAWG API. **Requieren que el servidor esté corriendo** y hacen llamadas reales a la API.

**Ejecutar:**
```bash
python Test/test_rawg_integration.py
```

**Incluye:**
- Importar videojuego desde RAWG
- Importar múltiples videojuegos (batch)
- Búsqueda híbrida (local + RAWG)
- Obtener videojuego enriquecido
- Sincronización asíncrona manual

**Requisitos:**
- Servidor Flask corriendo en `http://localhost:5000`
- Variable de entorno `RAWG_API_KEY` configurada
- Redis configurado (opcional, para caché)

### 2. Tests Unitarios (`test_services.py`)

Tests que verifican la lógica de servicios y mappers usando mocks. **No requieren servidor ni API real**.

**Ejecutar:**
```bash
python Test/test_services.py
```

O con pytest:
```bash
pytest Test/test_services.py -v
```

**Incluye:**
- Tests de `RAWGMapper` (transformación de datos)
- Tests de `RAWGService` (con mocks)
- Tests de `GameService` (con mocks)

### 3. Tests de Endpoints (`test_all_endpoints.py`) ⭐ NUEVO

Tests completos para **todos los endpoints** usando Flask test client. **No requieren servidor** y son muy rápidos.

**Ejecutar:**
```bash
python Test/test_all_endpoints.py
# O con pytest
pytest Test/test_all_endpoints.py -v
```

**Incluye 25 tests cubriendo:**
- ✅ Endpoints básicos (CRUD): GET, POST, PUT, DELETE
- ✅ Endpoints de consulta: categorías, estadísticas, búsqueda avanzada
- ✅ Endpoints RAWG: importar, importar-batch, enriquecido, buscar
- ✅ Endpoints de sincronización: sync-manual, sync-status
- ✅ Casos de error: 404, 400, validaciones

**Ver detalles:** `Test/ENDPOINTS_TEST_SUMMARY.md`

### 4. Tests de Endpoints Básicos (`test_videojuegos_endpoints.py`)

Tests que verifican endpoints básicos. **Requieren que el servidor esté corriendo**.

**Ejecutar:**
```bash
python Test/test_videojuegos_endpoints.py
```

### 5. Tests del Modelo SyncLog (`test_synclog.py`) ⭐ NUEVO

Tests para el modelo SyncLog que registra sincronizaciones.

**Ejecutar:**
```bash
python Test/test_synclog.py
```

**Incluye:**
- Creación y gestión de registros
- Marcado de éxito/fallo
- Estadísticas y consultas

## Configuración

### Variables de Entorno para Tests

Crear archivo `.env.test` o configurar:

```env
RAWG_API_KEY=tu_api_key_aqui
REDIS_URL=redis://localhost:6379/1  # DB diferente para tests
DATABASE_URL=postgresql://user:pass@localhost:5432/test_db
FLASK_DEBUG=True
```

### Instalar Dependencias de Testing

```bash
pip install pytest pytest-flask pytest-mock
```

## Ejecutar Todos los Tests

### Opción 1: Scripts Python individuales

```bash
# Tests básicos
python Test/test_videojuegos_endpoints.py

# Tests de RAWG
python Test/test_rawg_integration.py

# Tests unitarios
python Test/test_services.py
```

### Opción 2: Pytest (recomendado)

```bash
# Todos los tests (48 tests)
pytest Test/ -v

# Solo tests de endpoints (25 tests, rápidos)
pytest Test/test_all_endpoints.py -v

# Solo tests unitarios (16 tests)
pytest Test/test_services.py Test/test_synclog.py -v

# Con cobertura
pytest Test/ --cov=src --cov-report=html
```

### Opción 3: Scripts Específicos

```bash
# Tests de endpoints completos
python Test/test_all_endpoints.py

# Tests unitarios
python Test/test_services.py
python Test/test_synclog.py
```

## Tests con Mocks

Los tests unitarios usan mocks para evitar llamadas reales a APIs:

```python
@patch('src.Services.RAWGService.RAWGService._make_request')
def test_search_games(self, mock_request):
    mock_request.return_value = {'results': [...]}
    # Test sin llamada real a API
```

## Tests de Integración

Los tests de integración hacen llamadas reales y requieren:

1. **Servidor Flask corriendo:**
   ```bash
   python app.py
   ```

2. **API Key de RAWG configurada:**
   ```bash
   export RAWG_API_KEY=tu_key
   ```

3. **Base de datos inicializada:**
   ```bash
   python Test/init_db.py
   ```

## Mejores Prácticas

1. **Ejecutar tests unitarios primero** (más rápidos, no requieren servidor)
2. **Ejecutar tests de integración después** (más lentos, requieren configuración)
3. **Usar mocks** para tests unitarios cuando sea posible
4. **Limpiar datos de prueba** después de cada test
5. **Usar base de datos de prueba** separada de producción

## Troubleshooting

### Error: "No se pudo conectar al servidor"
- Asegúrate de que Flask esté corriendo en `http://localhost:5000`
- Verifica que no haya otro proceso usando el puerto 5000

### Error: "RAWG_API_KEY no configurada"
- Configura la variable de entorno `RAWG_API_KEY`
- O agrega al archivo `.env`

### Error: "ModuleNotFoundError: No module named 'pytest'"
- Instala pytest: `pip install pytest pytest-flask`

### Tests de Celery fallan
- Asegúrate de que Redis esté corriendo
- O configura Celery para usar un broker de prueba

## Cobertura de Código

Para ver la cobertura de tests:

```bash
pip install pytest-cov
pytest Test/ --cov=src --cov-report=html
```

Esto generará un reporte HTML en `htmlcov/index.html`.

## Agregar Nuevos Tests

1. **Tests unitarios**: Agregar a `test_services.py` o crear nuevo archivo `test_*.py`
2. **Tests de integración**: Agregar a `test_rawg_integration.py`
3. **Tests de endpoints**: Agregar a `test_videojuegos_endpoints.py`

Ejemplo de nuevo test:

```python
def test_nuevo_endpoint():
    """Test para nuevo endpoint."""
    response = requests.get(f"{BASE_URL}/api/nuevo-endpoint")
    assert response.status_code == 200
```

