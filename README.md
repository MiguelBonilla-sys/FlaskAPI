# 🎮 API de Videojuegos con Swagger con listas

Una API REST completa y bien documentada para gestionar videojuegos con operaciones CRUD, construida con Flask y documentada con Swagger/OpenAPI.

## 🚀 Características

- ✅ **CRUD Completo**: Crear, leer, actualizar y eliminar videojuegos
- 🔍 **Búsqueda y Filtrado**: Buscar por nombre, filtrar por categoría
- 📊 **Validación de Datos**: Validación robusta de entrada
- 📚 **Documentación Swagger**: Interfaz interactiva para probar la API
- 🎯 **Respuestas Estandarizadas**: Formato consistente de respuestas JSON
- 🛡️ **Manejo de Errores**: Manejo elegante de errores y excepciones
- 🌐 **CORS Ready**: Preparado para aplicaciones web

## 📋 Requisitos

- Python 3.8+
- Flask 3.1.2
- Flasgger 0.9.7.1

## 🔧 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/MiguelBonilla-sys/FlaskAPI.git
   cd FlaskAPI
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

## 🌐 URLs Importantes

- **API Base**: `http://localhost:5000/api/`
- **Documentación Swagger**: `http://localhost:5000/apidocs/`
- **Información de la API**: `http://localhost:5000/api/`

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
- `GET /api/videojuegos?categoria=Acción` - Solo videojuegos de acción
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

- **nombre**: Requerido, cadena no vacía
- **categoria**: Requerido, cadena no vacía
- **precio**: Requerido, número >= 0
- **valoracion**: Requerido, número entre 0 y 10

## 🌐 Códigos de Estado HTTP

- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Datos inválidos
- `404 Not Found`: Recurso no encontrado
- `405 Method Not Allowed`: Método HTTP no permitido
- `500 Internal Server Error`: Error del servidor

## 🧪 Ejemplos de Uso

### Con curl

#### Obtener todos los videojuegos
```bash
curl -X GET http://localhost:5000/api/videojuegos
```

#### Crear un videojuego
```bash
curl -X POST http://localhost:5000/api/videojuegos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Cyberpunk 2077",
    "categoria": "RPG",
    "precio": 59.99,
    "valoracion": 8.5
  }'
```

#### Buscar videojuegos
```bash
curl "http://localhost:5000/api/videojuegos?buscar=zelda"
```

#### Filtrar por categoría
```bash
curl "http://localhost:5000/api/videojuegos?categoria=Aventura"
```

#### Actualizar un videojuego
```bash
curl -X PUT http://localhost:5000/api/videojuegos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "precio": 49.99
  }'
```

#### Eliminar un videojuego
```bash
curl -X DELETE http://localhost:5000/api/videojuegos/1
```

### Con Python (requests)

```python
import requests

# URL base de la API
BASE_URL = "http://localhost:5000/api"

# Obtener todos los videojuegos
response = requests.get(f"{BASE_URL}/videojuegos")
print(response.json())

# Crear un nuevo videojuego
nuevo_juego = {
    "nombre": "Elden Ring",
    "categoria": "RPG",
    "precio": 59.99,
    "valoracion": 9.6
}
response = requests.post(f"{BASE_URL}/videojuegos", json=nuevo_juego)
print(response.json())

# Buscar videojuegos
response = requests.get(f"{BASE_URL}/videojuegos?buscar=zelda")
print(response.json())
```

## 🎮 Datos de Ejemplo

La API viene precargada con 5 videojuegos de ejemplo:

1. **The Legend of Zelda: Breath of the Wild** - Aventura - $59.99 - ⭐9.7
2. **God of War** - Acción - $49.99 - ⭐9.5
3. **Minecraft** - Sandbox - $29.99 - ⭐9.0
4. **FIFA 23** - Deportes - $69.99 - ⭐8.2
5. **Among Us** - Multijugador - $4.99 - ⭐8.5

## 📁 Estructura del Proyecto

```
FlaskAPI/
├── app.py                          # Punto de entrada principal
├── requirements.txt                # Dependencias
├── README.md                      # Este archivo
├── LICENSE                        # Licencia del proyecto
└── src/
    ├── __init__.py
    ├── Routes.py                  # Configuración de rutas y Swagger
    ├── Utils.py                   # Utilidades y helpers
    ├── Config/
    │   └── __init__.py
    ├── Controllers/
    │   ├── __init__.py
    │   └── VideojuegoController.py # Controladores de videojuegos
    ├── Services/
    │   ├── __init__.py
    │   └── VideojuegoService.py   # Lógica de negocio
    ├── Models/
    │   ├── __init__.py
    │   └── Videojuego.py          # Modelo de datos
    └── Middlewares/
        ├── __init__.py
        └── error_handler.py       # Manejo de errores
```

## 🚀 Despliegue

### Variables de Entorno

Puedes configurar las siguientes variables de entorno:

```bash
FLASK_ENV=development  # o production
FLASK_DEBUG=True      # para desarrollo
```

### Docker (Opcional)

Si prefieres usar Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

```bash
# Construir imagen
docker build -t flask-videojuegos-api .

# Ejecutar contenedor
docker run -p 5000:5000 flask-videojuegos-api
```

## 🧪 Testing

Para probar la API puedes usar:

1. **Swagger UI**: `http://localhost:5000/apidocs/` (Recomendado)
2. **Postman**: Importa la collection desde Swagger
3. **curl**: Ver ejemplos arriba
4. **Python requests**: Ver ejemplo arriba



## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Miguel Bonilla**
- GitHub: [@MiguelBonilla-sys](https://github.com/MiguelBonilla-sys)

---

⭐ ¡No olvides dar una estrella al proyecto si te resultó útil!

🎮 **¡Happy Gaming!** 🎮
