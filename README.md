# 🎮 API de Videojuegos - Flask REST API

Una API REST completa desarrollada con Flask para la gestión de videojuegos, con documentación interactiva Swagger y base de datos PostgreSQL.

## 🚀 Características

- ✅ **API REST completa** con operaciones CRUD
- 📚 **Documentación interactiva** con Swagger/Flasgger
- 🗄️ **Base de datos PostgreSQL** con SQLAlchemy
- 🔧 **Arquitectura modular**
- 🛡️ **Manejo robusto de errores**
- ✔️ **Validación de datos**
- 🔍 **Filtros y búsqueda**
- 📊 **Endpoints de estadísticas**

## 📋 Requisitos

- Python 3.8+
- PostgreSQL (Railway o local)
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd FlaskAPI
```

### 2. Crear entorno virtual
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```


### 4. Inicializar la base de datos
```bash
python init_db.py
```

### 5. Ejecutar la aplicación
```bash
python app.py
```

## 🌐 URLs Importantes

- **API Base**: `http://localhost:5000/api/`
- **Documentación Swagger**: `http://localhost:5000/apidocs/`
- **Información de la API**: `http://localhost:5000/api/`
- **Health Check**: `http://localhost:5000/health`

## 📖 Documentación Interactiva

Visita `http://localhost:5000/apidocs/` para acceder a la documentación interactiva de Swagger donde puedes:

- 📋 Ver todos los endpoints disponibles
- 🧪 Probar las APIs directamente desde el navegador
- 📝 Ver ejemplos de requests y responses
- 🔍 Explorar los modelos de datos
- 📊 Entender los códigos de estado HTTP

## 🎯 Endpoints Disponibles

### 1. Información de la API
```
GET /api/
```
Devuelve información básica de la API y lista de endpoints disponibles.

### 2. Obtener todos los videojuegos
```
GET /api/videojuegos
```
Parámetros de consulta opcionales:
- `categoria`: Filtra videojuegos por categoría
- `buscar`: Busca en nombre y categoría

**Ejemplos:**
- `GET /api/videojuegos` - Todos los videojuegos
- `GET /api/videojuegos?categoria=RPG` - Solo videojuegos de RPG
- `GET /api/videojuegos?buscar=zelda` - Buscar videojuegos que contengan "zelda"

### 3. Obtener un videojuego específico
```
GET /api/videojuegos/{id}
```

**Ejemplo:**
- `GET /api/videojuegos/1` - Obtiene el videojuego con ID 1

### 4. Crear un nuevo videojuego
```
POST /api/videojuegos
Content-Type: application/json

{
    "nombre": "The Witcher 3",
    "categoria": "RPG",
    "precio": 39.99,
    "valoracion": 9.3
}
```

### 5. Actualizar un videojuego
```
PUT /api/videojuegos/{id}
Content-Type: application/json

{
    "precio": 29.99,
    "valoracion": 9.5
}
```
Nota: Puedes enviar solo los campos que quieres actualizar.

### 6. Eliminar un videojuego
```
DELETE /api/videojuegos/{id}
```

### 7. Obtener categorías
```
GET /api/videojuegos/categorias
```
Devuelve todas las categorías únicas de videojuegos.

### 8. Obtener estadísticas
```
GET /api/videojuegos/estadisticas
```
Devuelve estadísticas básicas como total de videojuegos, categorías únicas, precio promedio, etc.

## 📊 Modelo de Datos

### Videojuego
```json
{
    "id": 1,
    "nombre": "The Legend of Zelda: Breath of the Wild",
    "categoria": "Aventura",
    "precio": 59.99,
    "valoracion": 9.7,
    "fecha_creacion": "2024-08-30T10:30:00.123456",
    "fecha_actualizacion": "2024-08-30T10:30:00.123456"
}
```

### Respuesta de la API
```json
{
    "success": true,
    "message": "Descripción de la operación",
    "data": { /* datos solicitados */ },
    "count": 5, // solo para listas
    "timestamp": "2024-08-30T10:30:00.123456"
}
```

## ✅ Validaciones

- **nombre**: Requerido, cadena no vacía, máximo 100 caracteres, único
- **categoria**: Requerido, cadena no vacía, máximo 50 caracteres
- **precio**: Requerido, número >= 0
- **valoracion**: Requerido, número entre 0 y 10

## 🌐 Códigos de Estado HTTP

- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Datos inválidos o petición incorrecta
- `404 Not Found`: Recurso no encontrado
- `405 Method Not Allowed`: Método HTTP no permitido
- `422 Unprocessable Entity`: Entidad no procesable
- `500 Internal Server Error`: Error del servidor

## 📁 Estructura del Proyecto

```
FlaskAPI/
├── app.py                          # Aplicación principal
├── init_db.py                      # Script de inicialización
├── requirements.txt                # Dependencias
├── .env                           # Variables de entorno
├── README.md                      # Documentación
└── src/
    ├── __init__.py
    ├── Routes.py                  # Definición de rutas y Swagger
    ├── Utils.py                   # Utilidades generales
    ├── Config/
    │   ├── __init__.py
    │   └── Database.py            # Configuración de base de datos
    ├── Controllers/
    │   ├── __init__.py
    │   └── VideojuegoController.py # Controlador de videojuegos
    ├── Models/
    │   ├── __init__.py
    │   └── Videojuego.py          # Modelo de datos
    ├── Services/
    │   ├── __init__.py
    │   └── VideojuegoService.py   # Lógica de negocio
    └── Middlewares/
        ├── __init__.py
        └── error_handler.py       # Manejo de errores
```



### Migraciones de base de datos
```bash
# Generar migración
flask db migrate -m "Descripción del cambio"

# Aplicar migración
flask db upgrade
```

## 🚀 Despliegue

### Variables de entorno para producción
```env
FLASK_DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-segura
```

### Comandos útiles
```bash
# Verificar estado de la aplicación
curl http://localhost:5000/health

# Probar endpoint de videojuegos
curl http://localhost:5000/api/videojuegos

# Crear un videojuego
curl -X POST http://localhost:5000/api/videojuegos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Nuevo Juego","categoria":"Acción","precio":49.99,"valoracion":8.5}'
```



## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.



## 🔗 Enlaces

- [Documentación de Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://sqlalchemy.org/)
- [Flasgger](https://github.com/flasgger/flasgger)
- [Railway](https://railway.app/)
