"""
Tests para integración con RAWG API.
Incluye tests para importación, búsqueda híbrida y enriquecimiento de datos.
"""
import os
import sys
import requests
import json
from unittest.mock import patch, MagicMock

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:5000"

def test_importar_externa():
    """Test para importar un videojuego desde RAWG."""
    print("\n🧪 Test: Importar videojuego desde RAWG")
    print("-" * 60)
    
    try:
        # Datos de prueba - usar un ID conocido de RAWG (ej: Grand Theft Auto V = 3498)
        test_data = {
            "external_id": "3498"  # GTA V en RAWG
        }
        
        response = requests.post(
            f"{BASE_URL}/api/videojuegos/importar-externa",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [201, 200]:
            data = response.json()
            game = data.get('data', {})
            print(f"✅ Videojuego importado exitosamente")
            print(f"   - ID Local: {game.get('id')}")
            print(f"   - Nombre: {game.get('nombre')}")
            print(f"   - External ID: {game.get('external_id')}")
            print(f"   - API Source: {game.get('api_source')}")
            print(f"   - Categoría: {game.get('categoria')}")
            print(f"   - Valoración: {game.get('valoracion')}")
            print(f"   - Descripción: {game.get('descripcion', '')[:100]}...")
            print(f"   - Imagen URL: {game.get('imagen_url', 'N/A')[:50]}...")
            return game.get('id')
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que la aplicación esté ejecutándose")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return None

def test_importar_batch():
    """Test para importar múltiples videojuegos desde RAWG."""
    print("\n🧪 Test: Importar múltiples videojuegos (batch)")
    print("-" * 60)
    
    try:
        # IDs conocidos de RAWG
        test_data = {
            "games": [
                {"external_id": "3328"},  # The Witcher 3
                {"external_id": "3498"},  # GTA V
                {"external_id": "5286"}   # Tomb Raider
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/api/videojuegos/importar-batch",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [201, 207]:
            data = response.json()
            results = data.get('data', {})
            print(f"✅ Importación batch completada")
            print(f"   - Exitosos: {len(results.get('success', []))}")
            print(f"   - Fallidos: {len(results.get('failed', []))}")
            print(f"   - Omitidos: {len(results.get('skipped', []))}")
            
            if results.get('success'):
                print(f"\n   Juegos importados:")
                for game in results['success'][:3]:  # Mostrar primeros 3
                    print(f"     - {game.get('nombre')} (ID: {game.get('id')})")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_buscar_hibrida():
    """Test para búsqueda híbrida (local + RAWG)."""
    print("\n🧪 Test: Búsqueda híbrida")
    print("-" * 60)
    
    try:
        # Búsqueda solo local
        print("📋 Búsqueda solo local...")
        response = requests.get(
            f"{BASE_URL}/api/videojuegos/buscar?q=zelda&include_external=false"
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('data', {})
            print(f"✅ Búsqueda local: {len(results.get('local', []))} resultados")
        
        # Búsqueda híbrida (local + externa)
        print("\n📋 Búsqueda híbrida (local + RAWG)...")
        response = requests.get(
            f"{BASE_URL}/api/videojuegos/buscar?q=zelda&include_external=true"
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('data', {})
            local_count = len(results.get('local', []))
            external_count = len(results.get('external', []))
            
            print(f"✅ Búsqueda híbrida completada")
            print(f"   - Resultados locales: {local_count}")
            print(f"   - Resultados externos (RAWG): {external_count}")
            
            if results.get('external'):
                print(f"\n   Primeros resultados externos:")
                for ext in results['external'][:3]:
                    print(f"     - {ext.get('nombre')} (ID RAWG: {ext.get('external_id')})")
                    print(f"       Categoría: {ext.get('categoria')}, Valoración: {ext.get('valoracion')}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_enriquecido():
    """Test para obtener videojuego enriquecido con datos de RAWG."""
    print("\n🧪 Test: Obtener videojuego enriquecido")
    print("-" * 60)
    
    try:
        # Primero necesitamos un videojuego con external_id
        # Intentar obtener el primero que tenga external_id
        response = requests.get(f"{BASE_URL}/api/videojuegos")
        
        if response.status_code == 200:
            data = response.json()
            games = data.get('data', [])
            
            # Buscar un juego con external_id
            game_with_external = None
            for game in games:
                if game.get('external_id'):
                    game_with_external = game
                    break
            
            if not game_with_external:
                print("⚠️  No hay juegos con external_id. Importa uno primero.")
                return False
            
            game_id = game_with_external.get('id')
            print(f"📋 Probando con juego ID: {game_id} ({game_with_external.get('nombre')})")
            
            # Obtener versión enriquecida
            response = requests.get(f"{BASE_URL}/api/videojuegos/{game_id}/enriquecido")
            
            if response.status_code == 200:
                data = response.json()
                game = data.get('data', {})
                
                print(f"✅ Juego enriquecido obtenido")
                print(f"   - Nombre: {game.get('nombre')}")
                print(f"   - Screenshots: {len(game.get('screenshots', []))} imágenes")
                print(f"   - Plataformas: {len(game.get('plataformas', []))} plataformas")
                print(f"   - Tags: {len(game.get('tags', []))} tags")
                
                if game.get('screenshots'):
                    print(f"\n   Primeros screenshots:")
                    for screenshot in game['screenshots'][:2]:
                        print(f"     - {screenshot[:80]}...")
                
                if game.get('plataformas'):
                    print(f"\n   Plataformas: {', '.join(game['plataformas'][:5])}")
                
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                return False
        else:
            print(f"❌ Error al obtener lista de juegos: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_sync_manual():
    """Test para sincronización asíncrona manual."""
    print("\n🧪 Test: Sincronización asíncrona manual")
    print("-" * 60)
    
    try:
        test_data = {
            "external_id": "3328"  # The Witcher 3
        }
        
        # Iniciar sincronización
        response = requests.post(
            f"{BASE_URL}/api/videojuegos/sync-manual",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 202:
            data = response.json()
            task_id = data.get('data', {}).get('task_id')
            status_url = data.get('data', {}).get('status_url')
            
            print(f"✅ Sincronización iniciada")
            print(f"   - Task ID: {task_id}")
            print(f"   - Status URL: {status_url}")
            
            # Consultar estado
            print(f"\n📋 Consultando estado de sincronización...")
            import time
            time.sleep(2)  # Esperar un poco
            
            response = requests.get(f"{BASE_URL}{status_url}")
            
            if response.status_code == 200:
                status_data = response.json()
                status = status_data.get('data', {}).get('status')
                print(f"   - Estado: {status}")
                
                if status == 'completed':
                    result = status_data.get('data', {}).get('result', {})
                    print(f"   - Game ID sincronizado: {result.get('game_id')}")
                
                return True
            else:
                print(f"⚠️  No se pudo consultar estado: {response.status_code}")
                return True  # La tarea se inició correctamente
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def run_all_tests():
    """Ejecuta todos los tests de integración RAWG."""
    print("=" * 60)
    print("🧪 TESTS DE INTEGRACIÓN RAWG API")
    print("=" * 60)
    
    results = {
        'passed': 0,
        'failed': 0,
        'total': 5
    }
    
    # Test 1: Importar externa
    if test_importar_externa():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 2: Importar batch
    if test_importar_batch():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 3: Búsqueda híbrida
    if test_buscar_hibrida():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 4: Obtener enriquecido
    if test_get_enriquecido():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 5: Sync manual
    if test_sync_manual():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE TESTS")
    print("=" * 60)
    print(f"✅ Pasados: {results['passed']}/{results['total']}")
    print(f"❌ Fallidos: {results['failed']}/{results['total']}")
    print(f"📈 Tasa de éxito: {(results['passed']/results['total']*100):.1f}%")
    
    return results['failed'] == 0

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

