"""
Script para probar endpoints en vivo (servidor corriendo).
Ejecuta pruebas contra un servidor Flask en ejecución.
"""
import requests
import json
import sys
from datetime import datetime

# URL base del servidor
BASE_URL = "http://localhost:5000"

def print_section(title):
    """Imprime un separador de sección."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_test(name, response, expected_status=200):
    """Imprime el resultado de un test."""
    status_icon = "✅" if response.status_code == expected_status else "❌"
    print(f"{status_icon} {name}")
    print(f"   Status: {response.status_code} (esperado: {expected_status})")
    
    if response.status_code != expected_status:
        try:
            error_data = response.json()
            print(f"   Error: {error_data.get('message', 'Unknown error')}")
        except:
            print(f"   Error: {response.text[:100]}")
    
    return response.status_code == expected_status

def test_health_endpoints():
    """Prueba los endpoints de health check."""
    print_section("HEALTH CHECK")
    
    # Health general
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print_test("GET /api/health", response)
        if response.status_code == 200:
            data = response.json()
            print(f"   Status general: {data.get('status')}")
            print(f"   Cache: {data.get('services', {}).get('cache', {}).get('status')}")
            print(f"   Database: {data.get('services', {}).get('database', {}).get('status')}")
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo en http://localhost:5000")
        return False
    
    # Health Redis específico
    try:
        response = requests.get(f"{BASE_URL}/api/health/redis")
        print_test("GET /api/health/redis", response)
        if response.status_code == 200:
            data = response.json()
            print(f"   Redis Status: {data.get('status')}")
            print(f"   Cache Type: {data.get('type')}")
            if 'redis_version' in data:
                print(f"   Redis Version: {data.get('redis_version')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    return True

def test_basic_endpoints():
    """Prueba endpoints básicos de videojuegos."""
    print_section("ENDPOINTS BÁSICOS")
    
    # GET /api/videojuegos
    response = requests.get(f"{BASE_URL}/api/videojuegos")
    print_test("GET /api/videojuegos", response)
    if response.status_code == 200:
        data = response.json()
        count = data.get('count', len(data.get('data', [])))
        print(f"   Videojuegos encontrados: {count}")
    
    # GET /api/videojuegos/categorias
    response = requests.get(f"{BASE_URL}/api/videojuegos/categorias")
    print_test("GET /api/videojuegos/categorias", response)
    if response.status_code == 200:
        data = response.json()
        categorias = data.get('data', [])
        print(f"   Categorías: {len(categorias)}")
        if categorias:
            print(f"   Ejemplos: {', '.join(categorias[:5])}")
    
    # GET /api/videojuegos/estadisticas
    response = requests.get(f"{BASE_URL}/api/videojuegos/estadisticas")
    print_test("GET /api/videojuegos/estadisticas", response)
    if response.status_code == 200:
        data = response.json()
        stats = data.get('data', {})
        print(f"   Total videojuegos: {stats.get('total_videojuegos', 0)}")
        print(f"   Precio promedio: ${stats.get('precio_promedio', 0):.2f}")
    
    # GET /api/videojuegos con filtros
    response = requests.get(f"{BASE_URL}/api/videojuegos?page=1&per_page=5")
    print_test("GET /api/videojuegos (con paginación)", response)

def test_crud_endpoints():
    """Prueba endpoints CRUD."""
    print_section("ENDPOINTS CRUD")
    
    # Crear videojuego de prueba
    nuevo_videojuego = {
        "nombre": f"Test Game {datetime.now().strftime('%H%M%S')}",
        "categoria": "Test",
        "precio": 29.99,
        "valoracion": 8.5
    }
    
    response = requests.post(
        f"{BASE_URL}/api/videojuegos",
        json=nuevo_videojuego,
        headers={'Content-Type': 'application/json'}
    )
    print_test("POST /api/videojuegos (crear)", response, 201)
    
    if response.status_code == 201:
        data = response.json()
        game_id = data.get('data', {}).get('id')
        print(f"   ID creado: {game_id}")
        
        if game_id:
            # GET por ID
            response = requests.get(f"{BASE_URL}/api/videojuegos/{game_id}")
            print_test(f"GET /api/videojuegos/{game_id}", response)
            
            # UPDATE
            update_data = {"precio": 19.99}
            response = requests.put(
                f"{BASE_URL}/api/videojuegos/{game_id}",
                json=update_data,
                headers={'Content-Type': 'application/json'}
            )
            print_test(f"PUT /api/videojuegos/{game_id} (actualizar)", response)
            
            # DELETE
            response = requests.delete(f"{BASE_URL}/api/videojuegos/{game_id}")
            print_test(f"DELETE /api/videojuegos/{game_id}", response)
    else:
        print("   ⚠️ No se pudo crear videojuego, saltando pruebas CRUD")

def test_rawg_endpoints():
    """Prueba endpoints de integración RAWG."""
    print_section("ENDPOINTS RAWG")
    
    # Búsqueda híbrida
    response = requests.get(f"{BASE_URL}/api/videojuegos/buscar?q=zelda&include_external=false")
    print_test("GET /api/videojuegos/buscar (búsqueda híbrida)", response)
    if response.status_code == 200:
        data = response.json()
        local = len(data.get('data', {}).get('local', []))
        external = len(data.get('data', {}).get('external', []))
        print(f"   Resultados locales: {local}")
        print(f"   Resultados externos: {external}")
    
    # Importar desde RAWG (usando un ID conocido de RAWG)
    # The Legend of Zelda: Breath of the Wild tiene ID 3328 en RAWG
    import_data = {"external_id": "3328"}
    response = requests.post(
        f"{BASE_URL}/api/videojuegos/importar-externa",
        json=import_data,
        headers={'Content-Type': 'application/json'}
    )
    print_test("POST /api/videojuegos/importar-externa", response, 201)
    
    if response.status_code == 201:
        data = response.json()
        game_id = data.get('data', {}).get('id')
        print(f"   Juego importado ID: {game_id}")
        
        if game_id:
            # GET enriquecido
            response = requests.get(f"{BASE_URL}/api/videojuegos/{game_id}/enriquecido")
            print_test(f"GET /api/videojuegos/{game_id}/enriquecido", response)
            if response.status_code == 200:
                data = response.json()
                game_data = data.get('data', {})
                print(f"   Nombre: {game_data.get('nombre')}")
                if 'screenshots' in game_data:
                    print(f"   Screenshots: {len(game_data.get('screenshots', []))}")

def test_search_endpoints():
    """Prueba endpoints de búsqueda."""
    print_section("BÚSQUEDA")
    
    # Búsqueda avanzada
    response = requests.get(f"{BASE_URL}/api/videojuegos/busqueda-avanzada?categoria=Test")
    print_test("GET /api/videojuegos/busqueda-avanzada", response)
    
    # Búsqueda con múltiples filtros
    response = requests.get(
        f"{BASE_URL}/api/videojuegos/busqueda-avanzada?precio_min=20&precio_max=50"
    )
    print_test("GET /api/videojuegos/busqueda-avanzada (con filtros)", response)

def test_error_cases():
    """Prueba casos de error."""
    print_section("CASOS DE ERROR")
    
    # GET videojuego inexistente
    response = requests.get(f"{BASE_URL}/api/videojuegos/99999")
    print_test("GET /api/videojuegos/99999 (no existe)", response, 404)
    
    # POST con datos inválidos
    invalid_data = {"nombre": ""}
    response = requests.post(
        f"{BASE_URL}/api/videojuegos",
        json=invalid_data,
        headers={'Content-Type': 'application/json'}
    )
    print_test("POST /api/videojuegos (datos inválidos)", response, 400)
    
    # Búsqueda sin parámetro requerido
    response = requests.get(f"{BASE_URL}/api/videojuegos/buscar")
    print_test("GET /api/videojuegos/buscar (sin parámetro q)", response, 400)

def main():
    """Ejecuta todas las pruebas."""
    print("\n" + "=" * 60)
    print("  PRUEBAS DE ENDPOINTS EN VIVO")
    print("=" * 60)
    print(f"Servidor: {BASE_URL}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'total': 0,
        'passed': 0,
        'failed': 0
    }
    
    try:
        # Health check primero
        if not test_health_endpoints():
            print("\n❌ El servidor no está disponible. Asegúrate de que esté corriendo.")
            return
        
        # Resto de pruebas
        test_basic_endpoints()
        test_crud_endpoints()
        test_rawg_endpoints()
        test_search_endpoints()
        test_error_cases()
        
        print_section("RESUMEN")
        print("✅ Pruebas completadas")
        print("\n💡 Para ver detalles de cada endpoint, revisa la documentación:")
        print(f"   {BASE_URL}/apidocs/")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

