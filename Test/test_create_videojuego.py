"""
Test rápido para verificar el endpoint POST /videojuegos
"""
import os
import sys
import requests
import json

# Test del endpoint POST
def test_create_videojuego():
    base_url = "http://localhost:5000"
    
    print("🧪 Probando POST /videojuegos...")
    
    # Datos de prueba
    nuevo_videojuego = {
        "nombre": "Test Game - " + str(hash("test")),
        "categoria": "Prueba",
        "precio": 25.99,
        "valoracion": 8.0,
        "desarrolladora_id": 1
    }
    
    try:
        response = requests.post(
            f"{base_url}/videojuegos",
            json=nuevo_videojuego,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            data = response.json()
            videojuego = data.get('data', {})
            print("✅ Videojuego creado exitosamente!")
            print(f"   - ID: {videojuego.get('id')}")
            print(f"   - Nombre: {videojuego.get('nombre')}")
            print(f"   - Desarrolladora ID: {videojuego.get('desarrolladora_id')}")
            
            desarrolladora = videojuego.get('desarrolladora')
            if desarrolladora:
                print(f"   - Desarrolladora: {desarrolladora.get('nombre')}")
                print(f"   - País: {desarrolladora.get('pais')}")
                print(f"   - Fundación: {desarrolladora.get('fundacion')}")
                print(f"   - Sitio web: {desarrolladora.get('sitio_web')}")
            
            return videojuego.get('id')
        else:
            print(f"❌ Error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que la aplicación esté ejecutándose en http://localhost:5000")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return None

if __name__ == '__main__':
    test_create_videojuego()