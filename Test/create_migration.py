"""
Script para crear migración de base de datos con Flask-Migrate.

Este script crea una migración para los nuevos campos agregados al modelo Videojuego
y el nuevo modelo SyncLog.

Uso:
    python create_migration.py
"""
import os
import sys
from flask import Flask
from flask_migrate import Migrate, migrate, init, upgrade

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from src.Config.Database import db, migrate as migrate_instance
from src.Models.Videojuego import Videojuego
from src.Models.Desarrolladora import Desarrolladora
from src.Models.SyncLog import SyncLog

def create_migration():
    """Crea la migración de base de datos."""
    app = create_app()
    
    with app.app_context():
        # Verificar si el directorio de migraciones existe
        migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
        
        if not os.path.exists(migrations_dir):
            print("Inicializando Flask-Migrate...")
            init()
            print("✓ Flask-Migrate inicializado")
        
        print("\nCreando migración para nuevos campos...")
        print("Campos nuevos en Videojuego:")
        print("  - external_id (String)")
        print("  - api_source (String)")
        print("  - last_synced (DateTime)")
        print("  - descripcion (Text)")
        print("  - imagen_url (String)")
        print("  - desarrollador (String)")
        print("\nNuevo modelo:")
        print("  - SyncLog (tabla sync_logs)")
        
        # Crear migración
        try:
            migrate(message="Add external API fields and SyncLog model")
            print("\n✓ Migración creada exitosamente")
            print("\nPara aplicar la migración, ejecuta:")
            print("  flask db upgrade")
            print("\nO desde Python:")
            print("  from app import create_app")
            print("  from src.Config.Database import db")
            print("  app = create_app()")
            print("  with app.app_context():")
            print("      db.create_all()  # Para desarrollo")
            print("      # O flask db upgrade  # Para producción")
        except Exception as e:
            print(f"\n✗ Error creando migración: {e}")
            print("\nNota: Si los campos ya existen, puedes aplicar la migración directamente:")
            print("  flask db upgrade")
            return False
    
    return True

if __name__ == '__main__':
    success = create_migration()
    sys.exit(0 if success else 1)

