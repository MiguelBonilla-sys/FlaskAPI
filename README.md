# 🎮 Flask API - Sistema de Gestión de Videojuegos

Una API REST robusta y escalable construida con Flask para la gestión de videojuegos, que incluye funcionalidades completas de CRUD, documentación automática con Swagger, y arquitectura modular siguiendo mejores prácticas.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Configuración del Entorno Virtual](#-configuración-del-entorno-virtual)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Documentación con Swagger](#-documentación-con-swagger)
- [Licencia](#-licencia)

## ✨ Características

- 🔧 **API REST completa** - Operaciones CRUD para videojuegos
- 📚 **Documentación automática** - Integración con Swagger/OpenAPI
- 🏗️ **Arquitectura modular** - Separación clara de responsabilidades
- 🐘 **Base de datos PostgreSQL** - Con SQLAlchemy como ORM
-  **Manejo de errores** - Sistema robusto de gestión de errores
- 📊 **Logs estructurados** - Sistema de logging avanzado
- 🌐 **CORS configurado** - Listo para aplicaciones frontend
- 🚀 **Despliegue en Railway** - Configuración incluida

## 🛠️ Tecnologías

- **Python 3.13** - Lenguaje base
- **Flask 3.1.2** - Framework web
- **SQLAlchemy 2.0.43** - ORM para base de datos
- **PostgreSQL** - Base de datos principal
- **Flasgger 0.9.7.1** - Documentación Swagger
- **Railway** - Plataforma de despliegue

## 🚀 Instalación

### Prerrequisitos

- Python 3.13+
- PostgreSQL
- pip (gestor de paquetes de Python)

### Clonación del repositorio

```bash
git clone https://github.com/tu-usuario/FlaskAPI.git
cd FlaskAPI
```

## 🔧 Configuración del Entorno Virtual

### ¿Qué es un entorno virtual (.venv)?

Un entorno virtual es un directorio que contiene una instalación aislada de Python junto con sus paquetes. Esto permite:

- **Aislamiento de dependencias**: Cada proyecto puede tener sus propias versiones de paquetes
- **Evitar conflictos**: No interfiere con otros proyectos Python
- **Facilitar despliegue**: Replica exactamente el entorno de desarrollo

### Creación y activación del entorno virtual

#### En Windows (CMD)

```cmd
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\activate

# Verificar activación (debería mostrar la ruta al entorno virtual)
where python
```

#### En Windows (PowerShell)

```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\Activate.ps1

# Si hay error de permisos, ejecutar primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### En Linux/macOS

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
source .venv/bin/activate
```

### Instalación de dependencias

```bash
# Con el entorno virtual activado
pip install -r requirements.txt
```

### Desactivar el entorno virtual

```bash
deactivate
```

## ⚙️ Configuración

### Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Configuración de Flask
FLASK_DEBUG=true
SECRET_KEY=tu-clave-secreta-muy-segura

# Configuración de base de datos
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/videojuegos_db

# Configuración del servidor
HOST=0.0.0.0
PORT=5000
```

### Inicialización de la base de datos

```bash
# Con el entorno virtual activado
python Test/init_db.py
```

## 🎯 Uso

### Desarrollo local

```bash
# Activar entorno virtual
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en:

- **API Base**: <http://localhost:5000/>
- **Documentación**: <http://localhost:5000/apidocs/>
- **Health Check**: <http://localhost:5000/health>

## 🌐 Endpoints de la API

### Endpoints Generales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Redirige a la documentación Swagger |
| GET | `/health` | Verificación de salud de la API |
| GET | `/api/info` | Información general de la API |

### Endpoints de Videojuegos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/videojuegos` | Obtener todos los videojuegos (con filtros opcionales) |
| GET | `/api/videojuegos/{id}` | Obtener un videojuego específico |
| POST | `/api/videojuegos` | Crear un nuevo videojuego |
| PUT | `/api/videojuegos/{id}` | Actualizar un videojuego existente |
| DELETE | `/api/videojuegos/{id}` | Eliminar un videojuego |
| GET | `/api/videojuegos/categorias` | Obtener todas las categorías disponibles |
| GET | `/api/videojuegos/estadisticas` | Obtener estadísticas de videojuegos |

### Filtros disponibles para GET /api/videojuegos

- `categoria`: Filtrar por categoría específica
- `precio_min`: Precio mínimo
- `precio_max`: Precio máximo
- `valoracion_min`: Valoración mínima
- `limit`: Límite de resultados
- `offset`: Número de resultados a omitir

### Ejemplo de uso

```bash
# Obtener todos los videojuegos
curl -X GET "http://localhost:5000/api/videojuegos"

# Filtrar por categoría
curl -X GET "http://localhost:5000/api/videojuegos?categoria=Aventura"

# Crear un nuevo videojuego
curl -X POST "http://localhost:5000/api/videojuegos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Elden Ring",
    "categoria": "RPG",
    "precio": 59.99,
    "valoracion": 9.5
  }'
```

## 📁 Estructura del Proyecto

```text
FlaskAPI/
├── app.py                          # Archivo principal de la aplicación Flask
├── LICENSE                         # Licencia del proyecto
├── Procfile                        # Configuración para despliegue en Railway
├── README.md                       # Documentación del proyecto
├── requirements.txt                # Dependencias del proyecto
├── runtime.txt                     # Versión específica de Python para Railway
├── src/                           # Código fuente principal
│   ├── __init__.py                # Hace que src sea un paquete Python
│   ├── Utils.py                   # Funciones de utilidad y helpers
│   ├── Config/                    # Configuraciones de la aplicación
│   │   ├── __init__.py
│   │   └── Database.py            # Configuración de base de datos y SQLAlchemy
│   ├── Controllers/               # Controladores de la lógica de negocio
│   │   ├── __init__.py
│   │   └── VideojuegoController.py # Controlador para operaciones de videojuegos
│   ├── Middlewares/               # Middlewares y manejo de errores
│   │   ├── __init__.py
│   │   └── error_handler.py       # Manejo global de errores y logging
│   ├── Models/                    # Modelos de datos (ORM)
│   │   ├── __init__.py
│   │   └── Videojuego.py         # Modelo de datos para videojuegos
│   ├── Routes/                    # Definición de rutas y endpoints
│   │   ├── __init__.py
│   │   ├── ApiRoutes.py          # Rutas generales (health, info)
│   │   └── VideojuegosRoutes.py  # Rutas específicas para videojuegos
│   ├── Schemas/                   # Esquemas para validación y documentación
│   │   ├── __init__.py
│   │   ├── ApiSchema.py          # Esquemas para endpoints generales
│   │   ├── SwaggerSchema.py      # Definiciones comunes de Swagger
│   │   └── VideojuegosSchema.py  # Esquemas para endpoints de videojuegos
│   ├── Services/                  # Capa de servicios y lógica de negocio
│   │   ├── __init__.py
│   │   └── VideojuegoService.py  # Servicios para operaciones de videojuegos
│   └── wsgi/                      # Configuración WSGI para producción
│       ├── __init__.py
│       └── wsgi.py               # Punto de entrada WSGI
└── Test/                          # Scripts de testing y utilidades
    └── init_db.py                # Script para inicialización de base de datos
```

### Descripción de Carpetas y Archivos

#### 📁 **src/** - Código fuente principal

Contiene todo el código de la aplicación organizado en módulos específicos.

#### 📁 **src/Config/** - Configuraciones

- **Database.py**: Configuración de SQLAlchemy, conexión a PostgreSQL, e inicialización de la base de datos.

#### 📁 **src/Controllers/** - Controladores

- **VideojuegoController.py**: Lógica de controlador que maneja las peticiones HTTP, valida datos y orquesta las operaciones de videojuegos.

#### 📁 **src/Middlewares/** - Middlewares

- **error_handler.py**: Manejo centralizado de errores, configuración de CORS, logging estructurado y decoradores para peticiones.

#### 📁 **src/Models/** - Modelos de datos

- **Videojuego.py**: Modelo SQLAlchemy que define la estructura de la tabla videojuegos, métodos de instancia y validaciones.

#### 📁 **src/Routes/** - Rutas y endpoints

- **ApiRoutes.py**: Rutas generales como health check e información de la API.
- **VideojuegosRoutes.py**: Todas las rutas específicas para operaciones CRUD de videojuegos.

#### 📁 **src/Schemas/** - Esquemas y documentación

- **ApiSchema.py**: Esquemas Swagger para endpoints generales.
- **SwaggerSchema.py**: Definiciones reutilizables y configuración base de Swagger.
- **VideojuegosSchema.py**: Esquemas detallados para todos los endpoints de videojuegos.

#### 📁 **src/Services/** - Servicios

- **VideojuegoService.py**: Lógica de negocio, operaciones de base de datos y validaciones de dominio.

#### 📁 **src/wsgi/** - Configuración WSGI

- **wsgi.py**: Punto de entrada para servidores de producción como Gunicorn.

#### 📁 **Test/** - Testing y utilidades

- **init_db.py**: Script para crear e inicializar la base de datos con datos de prueba.

#### 📄 **Archivos de configuración**

- **app.py**: Punto de entrada principal, factory pattern y configuración de la aplicación.
- **requirements.txt**: Todas las dependencias necesarias con versiones específicas.
- **Procfile**: Configuración para despliegue en Railway.
- **runtime.txt**: Especifica la versión de Python para Railway.

## 📖 Documentación con Swagger

### ¿Qué es Swagger y cómo se está usando?

**Swagger** (ahora OpenAPI) es una especificación para describir APIs REST de manera estándar. En este proyecto se utiliza **Flasgger**, que es una extensión de Flask que integra Swagger UI de forma automática.

### Características implementadas

1. **Documentación automática**: Cada endpoint está documentado con decoradores `@swag_from`
2. **Interfaz interactiva**: Swagger UI permite probar los endpoints directamente desde el navegador
3. **Esquemas reutilizables**: Definiciones comunes en `SwaggerSchema.py`
4. **Validación de datos**: Los esquemas sirven tanto para documentación como para validación

### Esquemas organizados por funcionalidad

- **ApiSchema.py**: Documentación para endpoints generales (health, info)
- **VideojuegosSchema.py**: Documentación completa para todas las operaciones CRUD
- **SwaggerSchema.py**: Definiciones de modelos reutilizables y configuración base

### Acceso a la documentación

- **URL**: `http://localhost:5000/apidocs/`
- **Características**:
  - Explorar todos los endpoints disponibles
  - Ver esquemas de petición y respuesta
  - Probar endpoints directamente desde la interfaz
  - Descargar especificación OpenAPI en JSON/YAML

### Configuración Swagger implementada

```python
# Configuración personalizada en SwaggerSchema.py
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
```

### Ejemplo de esquema implementado

```python
# Ejemplo de esquema para crear videojuego
create_videojuego_schema = {
    'tags': ['Videojuegos'],
    'summary': 'Crear un nuevo videojuego',
    'description': 'Crea un nuevo videojuego en la base de datos',
    'parameters': [
        {
            'name': 'videojuego',
            'in': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/VideojuegoInput'}
        }
    ],
    'responses': {
        201: {
            'description': 'Videojuego creado exitosamente',
            'schema': {'$ref': '#/definitions/ApiResponse'}
        }
    }
}
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

### Miguel Bonilla

- GitHub: [@MiguelBonilla-sys](https://github.com/MiguelBonilla-sys)

---

⭐ ¡No olvides dar una estrella si este proyecto te fue útil!
