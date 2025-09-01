"""
Archivo WSGI para despliegue en producción.
Este archivo es el punto de entrada para servidores como Gunicorn en Railway.
"""
import os
import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Importar la aplicación
from app import create_app

# Crear la aplicación WSGI
application = create_app()

# Variable que Railway y otros servicios buscan
app = application

if __name__ == "__main__":
    # Para pruebas locales del WSGI
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=False)
