# Configuración de seguridad para la API de Videojuegos

## Variables de entorno de seguridad (agregar a .env)

# API Keys para autenticación
ADMIN_API_KEY=admin_secure_key_2025_videogames_api
READONLY_API_KEY=readonly_key_2025_public_access
WRITER_API_KEY=writer_key_2025_content_manager

# Configuración de Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
RATE_LIMIT_BURST=10

# Configuración de seguridad adicional
SECURITY_HEADERS_ENABLED=true
CORS_ORIGINS=*
FLASK_DEBUG=false

## Ejemplo de uso de API Keys

### Lectura (sin API Key o con readonly)
```bash
# Sin autenticación (permitido para endpoints de lectura)
curl -X GET "http://localhost:5000/api/videojuegos"

# Con API key de solo lectura
curl -X GET "http://localhost:5000/api/videojuegos" \
  -H "X-API-Key: readonly_key_2025_public_access"
```

### Escritura (requiere API key con permisos de write)
```bash
# Crear videojuego (requiere permiso 'write')
curl -X POST "http://localhost:5000/api/videojuegos" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer writer_key_2025_content_manager" \
  -d '{
    "nombre": "Nuevo Juego",
    "categoria": "RPG",
    "precio": 49.99,
    "valoracion": 8.5
  }'
```

### Eliminación (requiere API key con permisos de delete)
```bash
# Eliminar videojuego (requiere permiso 'delete' - solo admin)
curl -X DELETE "http://localhost:5000/api/videojuegos/1" \
  -H "Authorization: Bearer admin_secure_key_2025_videogames_api"
```

## Rate Limiting implementado

- **GET requests**: 60 por minuto por IP
- **POST requests**: 10 por minuto por IP (estricto)
- **PUT requests**: 15 por minuto por IP (estricto)
- **DELETE requests**: 5 por minuto por IP (muy estricto)
- **Estadísticas**: Limitado por hora (endpoint costoso)

## Headers de respuesta

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1641024000
Retry-After: 30 (solo en 429)
```

## Códigos de error de seguridad

- **401**: API key faltante o inválida
- **403**: Permisos insuficientes
- **429**: Rate limit excedido

## Endpoints protegidos

- `POST /api/videojuegos` - Requiere permiso 'write'
- `PUT /api/videojuegos/{id}` - Requiere permiso 'write'
- `DELETE /api/videojuegos/{id}` - Requiere permiso 'delete'
- `POST /api/admin/generate-key` - Requiere permiso 'admin'

## Endpoints públicos (sin autenticación)

- `GET /health`
- `GET /api/`
- `GET /apidocs/`
- `GET /`
- `GET /api/videojuegos` (con rate limiting)
- `GET /api/videojuegos/{id}` (con rate limiting)
- `GET /api/videojuegos/categorias` (con rate limiting)
- `GET /api/videojuegos/estadisticas` (con rate limiting por hora)
