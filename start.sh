#!/bin/bash
# Script de inicio para Railway

# Configurar variables por defecto
export PORT=${PORT:-5000}
export WORKERS=${WORKERS:-4}
export TIMEOUT=${TIMEOUT:-120}

echo "🚀 Iniciando aplicación Flask en Railway"
echo "📍 Puerto: $PORT"
echo "👥 Workers: $WORKERS"
echo "⏱️  Timeout: $TIMEOUT"

# Ejecutar Gunicorn
exec gunicorn --bind "0.0.0.0:$PORT" --workers "$WORKERS" --timeout "$TIMEOUT" src.wsgi.wsgi:application
