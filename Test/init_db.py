"""
Script de inicialización para poblar la base de datos con datos de ejemplo.
"""
import os
import sys
from datetime import datetime

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from src.Config.Database import db
from src.Models.Videojuego import Videojuego

def create_sample_data():
    """
    Crea datos de ejemplo para la base de datos.
    """
    # Datos de ejemplo
    videojuegos_ejemplo = [
        {
            'nombre': 'The Legend of Zelda: Breath of the Wild',
            'categoria': 'Aventura',
            'precio': 59.99,
            'valoracion': 9.7
        },
        {
            'nombre': 'The Witcher 3: Wild Hunt',
            'categoria': 'RPG',
            'precio': 39.99,
            'valoracion': 9.3
        },
        {
            'nombre': 'God of War',
            'categoria': 'Acción',
            'precio': 49.99,
            'valoracion': 9.5
        },
        {
            'nombre': 'Cyberpunk 2077',
            'categoria': 'RPG',
            'precio': 59.99,
            'valoracion': 7.8
        },
        {
            'nombre': 'FIFA 24',
            'categoria': 'Deportes',
            'precio': 69.99,
            'valoracion': 8.2
        },
        {
            'nombre': 'Call of Duty: Modern Warfare II',
            'categoria': 'Acción',
            'precio': 69.99,
            'valoracion': 8.5
        },
        {
            'nombre': 'Elden Ring',
            'categoria': 'RPG',
            'precio': 59.99,
            'valoracion': 9.6
        },
        {
            'nombre': 'Spider-Man: Miles Morales',
            'categoria': 'Acción',
            'precio': 49.99,
            'valoracion': 8.8
        },
        {
            'nombre': 'Animal Crossing: New Horizons',
            'categoria': 'Simulación',
            'precio': 59.99,
            'valoracion': 9.0
        },
        {
            'nombre': 'Super Mario Odyssey',
            'categoria': 'Plataformas',
            'precio': 59.99,
            'valoracion': 9.4
        }
    ]
    
    try:
        # Limpiar datos existentes (opcional)
        print("🗑️  Limpiando datos existentes...")
        Videojuego.query.delete()
        
        # Crear nuevos videojuegos
        print("📦 Creando datos de ejemplo...")
        for data in videojuegos_ejemplo:
            videojuego = Videojuego(
                nombre=data['nombre'],
                categoria=data['categoria'],
                precio=data['precio'],
                valoracion=data['valoracion']
            )
            db.session.add(videojuego)
        
        # Confirmar cambios
        db.session.commit()
        
        print(f"✅ Se crearon {len(videojuegos_ejemplo)} videojuegos de ejemplo exitosamente")
        
        # Mostrar estadísticas
        total = Videojuego.query.count()
        categorias = db.session.query(Videojuego.categoria).distinct().count()
        
        print(f"📊 Estadísticas:")
        print(f"   - Total de videojuegos: {total}")
        print(f"   - Categorías únicas: {categorias}")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al crear datos de ejemplo: {str(e)}")
        return False
    
    return True

def main():
    """
    Función principal del script de inicialización.
    """
    print("🎮 Inicializando base de datos de videojuegos...")
    print("=" * 50)
    
    # Crear aplicación
    app = create_app()
    
    with app.app_context():
        try:
            # Crear tablas
            print("🔧 Creando tablas de la base de datos...")
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            
            # Crear datos de ejemplo
            success = create_sample_data()
            
            if success:
                print("=" * 50)
                print("🎉 ¡Inicialización completada exitosamente!")
                print("🚀 Puedes iniciar la aplicación con: python app.py")
                print("📚 Documentación disponible en: http://localhost:5000/apidocs/")
            else:
                print("❌ La inicialización falló")
                return 1
                
        except Exception as e:
            print(f"❌ Error durante la inicialización: {str(e)}")
            return 1
    
    return 0

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
