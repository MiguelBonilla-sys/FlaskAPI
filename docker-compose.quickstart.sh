#!/bin/bash
# Script rápido para iniciar Docker Compose

echo "🐳 Iniciando FlaskAPI con Docker Compose..."
echo ""

# Verificar si existe .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado"
    echo "📝 Creando .env desde .env.example..."
    cp .env.example .env
    echo "✅ Archivo .env creado. Por favor, edítalo con tus valores."
    echo ""
fi

# Construir e iniciar servicios
echo "🔨 Construyendo imágenes..."
docker-compose build

echo ""
echo "🚀 Iniciando servicios..."
docker-compose up -d

echo ""
echo "⏳ Esperando que los servicios estén listos..."
sleep 10

echo ""
echo "📊 Estado de servicios:"
docker-compose ps

echo ""
echo "✅ Servicios iniciados!"
echo ""
echo "📝 Comandos útiles:"
echo "  - Ver logs: docker-compose logs -f"
echo "  - Detener: docker-compose down"
echo "  - Reiniciar: docker-compose restart"
echo ""
echo "🌐 API disponible en: http://localhost:5000"
echo "📚 Swagger UI: http://localhost:5000/apidocs"

