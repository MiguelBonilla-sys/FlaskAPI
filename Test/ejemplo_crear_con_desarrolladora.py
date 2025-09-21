"""
Ejemplo completo de cómo crear un videojuego con desarrolladora
"""
import requests
import json

def ejemplo_crear_videojuego():
    base_url = "http://localhost:5000"
    
    print("🎮 Ejemplo: Crear videojuego con desarrolladora")
    print("=" * 50)
    
    # Paso 1: Obtener desarrolladoras disponibles
    print("📋 Paso 1: Obtener desarrolladoras disponibles...")
    try:
        response = requests.get(f"{base_url}/desarrolladoras")
        if response.status_code == 200:
            desarrolladoras = response.json()['data']
            print(f"✅ Encontradas {len(desarrolladoras)} desarrolladoras:")
            for dev in desarrolladoras[:5]:  # Mostrar solo las primeras 5
                print(f"   - ID: {dev['id']}, Nombre: {dev['nombre']}, País: {dev['pais']}")
            print()
            
            # Paso 2: Crear videojuego CON desarrolladora
            print("➕ Paso 2a: Crear videojuego CON desarrolladora...")
            nuevo_videojuego_con_dev = {
                "nombre": "Test Game CON Desarrolladora",
                "categoria": "Aventura",
                "precio": 45.99,
                "valoracion": 8.7,
                "desarrolladora_id": desarrolladoras[0]['id']  # Usar la primera desarrolladora
            }
            
            response = requests.post(
                f"{base_url}/videojuegos",
                json=nuevo_videojuego_con_dev,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                data = response.json()['data']
                print(f"✅ Videojuego creado con desarrolladora:")
                print(f"   - ID: {data['id']}")
                print(f"   - Nombre: {data['nombre']}")
                print(f"   - Desarrolladora: {data['desarrolladora']['nombre']}")
                print(f"   - País: {data['desarrolladora']['pais']}")
                print()
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
            # Paso 3: Crear videojuego SIN desarrolladora
            print("➕ Paso 2b: Crear videojuego SIN desarrolladora...")
            nuevo_videojuego_sin_dev = {
                "nombre": "Test Game SIN Desarrolladora",
                "categoria": "Indie",
                "precio": 19.99,
                "valoracion": 7.5
                # No incluir desarrolladora_id
            }
            
            response = requests.post(
                f"{base_url}/videojuegos",
                json=nuevo_videojuego_sin_dev,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                data = response.json()['data']
                print(f"✅ Videojuego creado sin desarrolladora:")
                print(f"   - ID: {data['id']}")
                print(f"   - Nombre: {data['nombre']}")
                print(f"   - Desarrolladora: {data['desarrolladora']}")  # Debe ser None
                print()
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        else:
            print(f"❌ Error al obtener desarrolladoras: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que la aplicación esté ejecutándose en http://localhost:5000")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
    
    print("=" * 50)
    print("📝 RESUMEN:")
    print("1. Usar GET /desarrolladoras para ver opciones")
    print("2. Copiar el ID de la desarrolladora deseada")
    print("3. Incluir desarrolladora_id en el POST (o omitirlo)")
    print("4. El campo desarrolladora_id es completamente opcional")

if __name__ == '__main__':
    ejemplo_crear_videojuego()