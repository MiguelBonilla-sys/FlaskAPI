# Usar Python 3.13 slim como base (más pequeña y eficiente)
FROM python:3.13-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema y crear entorno virtual
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar requirements y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar el código de la aplicación y configurar usuarios/permisos
COPY . .
RUN mkdir -p /app/logs && \
    adduser --disabled-password --gecos '' --shell /bin/bash user && \
    chown -R user:user /app && \
    chown -R user:user /opt/venv
USER user

# Exponer el puerto
EXPOSE 5000

# Comando de salud para Docker
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando por defecto (usar Gunicorn para producción)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "src.wsgi.wsgi:application"]
