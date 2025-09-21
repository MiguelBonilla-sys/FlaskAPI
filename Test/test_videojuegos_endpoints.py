"""
Script de prueba para verificar que todos los endpoints de videojuegos funcionan correctamente
con el nuevo modelo de desarrolladoras.
"""
import os
import sys
import requests
import json

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_endpoints():
    """
    Prueba todos los endpoints de videojuegos.
    """
    base_url = "http://localhost:5000"
    
    print("🧪 Iniciando pruebas de endpoints de videojuegos...")
    print("=" * 60)
    
    try:
        # 1. Probar GET /videojuegos
        print("📋 Probando GET /videojuegos...")
        response = requests.get(f"{base_url}/videojuegos")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Endpoint funcionando - {data.get('count', 0)} videojuegos encontrados")
            if data.get('data') and len(data['data']) > 0:
                videojuego = data['data'][0]
                print(f"   - Ejemplo: {videojuego.get('nombre')}")
                print(f"   - Desarrolladora: {videojuego.get('desarrolladora', {}).get('nombre', 'Sin desarrolladora')}")
        else:
            print(f"❌ Error: {response.status_code}")
        
        # 2. Probar GET /videojuegos con filtro por desarrolladora
        print("\n🔍 Probando GET /videojuegos?desarrolladora_id=1...")
        response = requests.get(f"{base_url}/videojuegos?desarrolladora_id=1")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Filtro por desarrolladora funcionando - {data.get('count', 0)} videojuegos encontrados")
        else:
            print(f"❌ Error: {response.status_code}")
        
        # 3. Probar búsqueda avanzada
        print("\n🔎 Probando GET /videojuegos/busqueda-avanzada...")
        response = requests.get(f"{base_url}/videojuegos/busqueda-avanzada?categoria=RPG&precio_min=30")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Búsqueda avanzada funcionando - {data.get('count', 0)} videojuegos encontrados")
        else:
            print(f"❌ Error: {response.status_code}")
        
        # 4. Probar GET /videojuegos/{id}
        print("\n📄 Probando GET /videojuegos/1...")
        response = requests.get(f"{base_url}/videojuegos/1")
        if response.status_code == 200:
            data = response.json()
            videojuego = data.get('data', {})
            print(f"✅ Obtener videojuego por ID funcionando")
            print(f"   - Nombre: {videojuego.get('nombre')}")
            desarrolladora = videojuego.get('desarrolladora')
            if desarrolladora:
                print(f"   - Desarrolladora: {desarrolladora.get('nombre')}")
                print(f"   - País: {desarrolladora.get('pais')}")
                print(f"   - Fundación: {desarrolladora.get('fundacion')}")
                print(f"   - Sitio web: {desarrolladora.get('sitio_web')}")
            else:
                print("   - Sin desarrolladora asociada")
        else:
            print(f"❌ Error: {response.status_code}")
        
        # 5. Probar POST /videojuegos (crear)
        print("\n➕ Probando POST /videojuegos...")
        nuevo_videojuego = {
            "nombre": "Videojuego de Prueba",
            "categoria": "Prueba",
            "precio": 29.99,
            "valoracion": 8.5,
            "desarrolladora_id": 1
        }
        response = requests.post(
            f"{base_url}/videojuegos", 
            json=nuevo_videojuego,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 201:
            data = response.json()
            videojuego_creado = data.get('data', {})
            print(f"✅ Crear videojuego funcionando")
            print(f"   - ID creado: {videojuego_creado.get('id')}")
            test_id = videojuego_creado.get('id')
            
            # 6. Probar PUT /videojuegos/{id} (actualizar)
            print(f"\n📝 Probando PUT /videojuegos/{test_id}...")
            actualizacion = {
                "nombre": "Videojuego de Prueba Actualizado",
                "precio": 19.99
            }
            response = requests.put(
                f"{base_url}/videojuegos/{test_id}",
                json=actualizacion,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                print("✅ Actualizar videojuego funcionando")
            else:
                print(f"❌ Error: {response.status_code}")
            
            # 7. Probar DELETE /videojuegos/{id}
            print(f"\n🗑️ Probando DELETE /videojuegos/{test_id}...")
            response = requests.delete(f"{base_url}/videojuegos/{test_id}")
            if response.status_code == 200:
                print("✅ Eliminar videojuego funcionando")
            else:
                print(f"❌ Error: {response.status_code}")
        else:
            print(f"❌ Error al crear: {response.status_code}")
            if response.text:
                print(f"   Respuesta: {response.text}")
        
        print("\n" + "=" * 60)
        print("🎉 Pruebas completadas!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que la aplicación esté ejecutándose en http://localhost:5000")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

if __name__ == '__main__':
    test_endpoints()