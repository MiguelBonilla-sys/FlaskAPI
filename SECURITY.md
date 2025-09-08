# Configuración de seguridad para la API de Videojuegos

## 🚀 CONFIGURACIÓN SIMPLIFICADA

La API funciona **perfectamente sin configuración adicional**. Todas las medidas de seguridad están implementadas con valores por defecto seguros.

## 🔒 Rate Limiting (Automático)

- **GET requests**: 60 por minuto por IP
- **POST requests**: 10 por minuto por IP (estricto)
- **PUT requests**: 15 por minuto por IP (estricto)
- **DELETE requests**: 5 por minuto por IP (muy estricto)
- **Estadísticas**: Limitado por hora (endpoint costoso)

## 🌐 Endpoints Públicos (Sin autenticación requerida)

- `GET /health` - Health check
- `GET /api/` - Información de la API
- `GET /apidocs/` - Documentación Swagger
- `GET /` - Redirige a documentación
- `GET /api/videojuegos` - Obtener videojuegos
- `GET /api/videojuegos/{id}` - Obtener videojuego específico
- `GET /api/videojuegos/categorias` - Obtener categorías
- `GET /api/videojuegos/estadisticas` - Obtener estadísticas
- `POST /api/videojuegos` - Crear videojuego (con rate limiting)
- `PUT /api/videojuegos/{id}` - Actualizar videojuego (con rate limiting)
- `DELETE /api/videojuegos/{id}` - Eliminar videojuego (con rate limiting)

## 📊 Uso Básico

```bash
# Obtener todos los videojuegos
curl -X GET "http://localhost:5000/api/videojuegos"

# Crear un nuevo videojuego
curl -X POST "http://localhost:5000/api/videojuegos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Nuevo Juego",
    "categoria": "RPG", 
    "precio": 49.99,
    "valoracion": 8.5
  }'

# Actualizar videojuego
curl -X PUT "http://localhost:5000/api/videojuegos/1" \
  -H "Content-Type: application/json" \
  -d '{
    "precio": 39.99
  }'

# Eliminar videojuego  
curl -X DELETE "http://localhost:5000/api/videojuegos/1"
```

## ⚙️ Configuración Opcional para Railway

Si quieres personalizar la configuración en Railway:

```env
# Rate limiting (opcional)
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100

# Flask (opcional)
FLASK_DEBUG=false
```

## 🛡️ Medidas de Seguridad Activas

- ✅ **Rate limiting** por IP
- ✅ **Validación de entrada** anti-inyección
- ✅ **Headers de seguridad** automáticos
- ✅ **Sanitización** de datos
- ✅ **Logging** de seguridad
- ✅ **Protección XSS/SQL injection**

## 📈 Headers de Respuesta

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1641024000
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

## 🎯 Códigos de Error

- **400**: Datos inválidos o malformados
- **429**: Rate limit excedido
- **500**: Error interno del servidor
