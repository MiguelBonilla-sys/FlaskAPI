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
from src.Models.Desarrolladora import Desarrolladora

def check_and_reset_database():
    """
    Verifica si existen datos en las tablas y las elimina/recrea si es necesario.
    """
    try:
        # Verificar si las tablas existen y tienen datos
        videojuegos_count = 0
        desarrolladoras_count = 0
        
        try:
            videojuegos_count = Videojuego.query.count()
            desarrolladoras_count = Desarrolladora.query.count()
        except Exception:
            # Las tablas no existen o hay error de estructura
            print("⚠️  Las tablas no existen o tienen estructura incorrecta")
            videojuegos_count = 0
            desarrolladoras_count = 0
        
        total_records = videojuegos_count + desarrolladoras_count
        
        if total_records > 0:
            print(f"🔍 Detectados {videojuegos_count} videojuegos y {desarrolladoras_count} desarrolladoras")
            print("🗑️  Eliminando datos existentes (método rápido)...")
            
            # Método más rápido: eliminar solo los datos, no las tablas
            try:
                # Para PostgreSQL usar TRUNCATE CASCADE
                db.session.execute(db.text("TRUNCATE TABLE videojuegos, desarrolladoras RESTART IDENTITY CASCADE"))
                db.session.commit()
                print("✅ Datos eliminados exitosamente (TRUNCATE)")
            except Exception:
                # Fallback para otros motores de BD o si TRUNCATE falla
                print("⚠️  TRUNCATE no disponible, usando DELETE...")
                db.session.rollback()
                
                # Eliminar datos con DELETE (orden importante por foreign keys)
                Videojuego.query.delete()
                Desarrolladora.query.delete()
                db.session.commit()
                print("✅ Datos eliminados exitosamente (DELETE)")
        else:
            print("📋 Base de datos vacía o tablas no existen")
        
        # Asegurar que las tablas existen con la estructura correcta
        print("🔧 Verificando estructura de tablas...")
        db.create_all()
        print("✅ Estructura de base de datos verificada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar/resetear la base de datos: {str(e)}")
        return False

def create_sample_data():
    """
    Crea datos de ejemplo para la base de datos.
    """
    # Datos de desarrolladoras
    desarrolladoras_ejemplo = [
        {
            'nombre': 'Nintendo',
            'pais': 'Japón',
            'fundacion': 18890923,  # 23 septiembre 1889
            'sitio_web': 'https://www.nintendo.com',
            'descripcion': 'Compañía japonesa de videojuegos conocida por Mario, Zelda y Pokémon'
        },
        {
            'nombre': 'CD Projekt RED',
            'pais': 'Polonia',
            'fundacion': 20020514,  # 14 mayo 2002
            'sitio_web': 'https://www.cdprojekt.com',
            'descripcion': 'Estudio polaco famoso por The Witcher y Cyberpunk 2077'
        },
        {
            'nombre': 'Santa Monica Studio',
            'pais': 'Estados Unidos',
            'fundacion': 19990101,  # 1 enero 1999
            'sitio_web': 'https://sms.playstation.com',
            'descripcion': 'Estudio estadounidense, parte de Sony Interactive Entertainment'
        },
        {
            'nombre': 'EA Sports',
            'pais': 'Estados Unidos',
            'fundacion': 19910101,  # 1 enero 1991
            'sitio_web': 'https://www.ea.com/ea-sports',
            'descripcion': 'División deportiva de Electronic Arts'
        },
        {
            'nombre': 'Activision',
            'pais': 'Estados Unidos',
            'fundacion': 19791001,  # 1 octubre 1979
            'sitio_web': 'https://www.activision.com',
            'descripcion': 'Gran empresa de videojuegos estadounidense'
        },
        {
            'nombre': 'FromSoftware',
            'pais': 'Japón',
            'fundacion': 19861101,  # 1 noviembre 1986
            'sitio_web': 'https://www.fromsoftware.jp',
            'descripcion': 'Estudio japonés conocido por juegos de dificultad extrema'
        },
        {
            'nombre': 'Insomniac Games',
            'pais': 'Estados Unidos',
            'fundacion': 19940101,  # 1 enero 1994
            'sitio_web': 'https://insomniac.games',
            'descripcion': 'Estudio estadounidense famoso por Spider-Man y Ratchet & Clank'
        }
    ]
    
    # Datos de videojuegos (actualizados con desarrolladora_id)
    videojuegos_ejemplo = [
        {
            'nombre': 'The Legend of Zelda: Breath of the Wild',
            'categoria': 'Aventura',
            'precio': 59.99,
            'valoracion': 9.7,
            'desarrolladora_nombre': 'Nintendo'
        },
        {
            'nombre': 'The Witcher 3: Wild Hunt',
            'categoria': 'RPG',
            'precio': 39.99,
            'valoracion': 9.3,
            'desarrolladora_nombre': 'CD Projekt RED'
        },
        {
            'nombre': 'God of War',
            'categoria': 'Acción',
            'precio': 49.99,
            'valoracion': 9.5,
            'desarrolladora_nombre': 'Santa Monica Studio'
        },
        {
            'nombre': 'Cyberpunk 2077',
            'categoria': 'RPG',
            'precio': 59.99,
            'valoracion': 7.8,
            'desarrolladora_nombre': 'CD Projekt RED'
        },
        {
            'nombre': 'FIFA 24',
            'categoria': 'Deportes',
            'precio': 69.99,
            'valoracion': 8.2,
            'desarrolladora_nombre': 'EA Sports'
        },
        {
            'nombre': 'Call of Duty: Modern Warfare II',
            'categoria': 'Acción',
            'precio': 69.99,
            'valoracion': 8.5,
            'desarrolladora_nombre': 'Activision'
        },
        {
            'nombre': 'Elden Ring',
            'categoria': 'RPG',
            'precio': 59.99,
            'valoracion': 9.6,
            'desarrolladora_nombre': 'FromSoftware'
        },
        {
            'nombre': 'Spider-Man: Miles Morales',
            'categoria': 'Acción',
            'precio': 49.99,
            'valoracion': 8.8,
            'desarrolladora_nombre': 'Insomniac Games'
        },
        {
            'nombre': 'Animal Crossing: New Horizons',
            'categoria': 'Simulación',
            'precio': 59.99,
            'valoracion': 9.0,
            'desarrolladora_nombre': 'Nintendo'
        },
        {
            'nombre': 'Super Mario Odyssey',
            'categoria': 'Plataformas',
            'precio': 59.99,
            'valoracion': 9.4,
            'desarrolladora_nombre': 'Nintendo'
        }
    ]
    
    try:
        # Crear desarrolladoras primero
        print("🏢 Creando desarrolladoras...")
        desarrolladoras_creadas = {}
        for data in desarrolladoras_ejemplo:
            desarrolladora = Desarrolladora(
                nombre=data['nombre'],
                pais=data['pais'],
                fundacion=data['fundacion'],
                sitio_web=data['sitio_web'],
                descripcion=data['descripcion']
            )
            db.session.add(desarrolladora)
            db.session.flush()  # Para obtener el ID
            desarrolladoras_creadas[data['nombre']] = desarrolladora.id
        
        # Crear videojuegos con desarrolladoras
        print("🎮 Creando videojuegos...")
        for data in videojuegos_ejemplo:
            desarrolladora_id = desarrolladoras_creadas.get(data['desarrolladora_nombre'])
            videojuego = Videojuego(
                nombre=data['nombre'],
                categoria=data['categoria'],
                precio=data['precio'],
                valoracion=data['valoracion'],
                desarrolladora_id=desarrolladora_id
            )
            db.session.add(videojuego)
        
        # Confirmar cambios
        db.session.commit()
        
        print(f"✅ Se crearon {len(desarrolladoras_ejemplo)} desarrolladoras exitosamente")
        print(f"✅ Se crearon {len(videojuegos_ejemplo)} videojuegos exitosamente")
        
        # Mostrar estadísticas
        total_videojuegos = Videojuego.query.count()
        total_desarrolladoras = Desarrolladora.query.count()
        categorias = db.session.query(Videojuego.categoria).distinct().count()
        
        print("📊 Estadísticas:")
        print(f"   - Total de videojuegos: {total_videojuegos}")
        print(f"   - Total de desarrolladoras: {total_desarrolladoras}")
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
    print("🎮 Inicializando base de datos de videojuegos y desarrolladoras...")
    print("=" * 60)
    
    # Crear aplicación
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar y resetear base de datos si tiene datos
            reset_success = check_and_reset_database()
            if not reset_success:
                print("❌ Error al preparar la base de datos")
                return 1
            
            # Crear datos de ejemplo
            success = create_sample_data()
            
            if success:
                print("=" * 60)
                print("🎉 ¡Inicialización completada exitosamente!")
                print("🚀 Puedes iniciar la aplicación con: python app.py")
                print("📚 Documentación disponible en: http://localhost:5000/apidocs/")
                print("🎮 Endpoints de videojuegos: /videojuegos")
                print("🏢 Endpoints de desarrolladoras: /desarrolladoras")
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
