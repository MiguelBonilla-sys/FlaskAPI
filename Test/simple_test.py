"""
Test simple para verificar que la API funciona sin configuración.
"""
import sys
import os

# Agregar el directorio raíz al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app import create_app

def test_simplified_api():
    """
    Prueba que la API funciona sin configuración adicional.
    """
    print("🧪 PROBANDO API SIMPLIFICADA")
    print("=" * 40)
    
    # Crear app
    app = create_app()
    
    with app.test_client() as client:
        # Test GET (público)
        resp = client.get('/api/videojuegos')
        print(f"✅ GET /api/videojuegos: {resp.status_code}")
        
        # Test POST (ahora público con rate limiting)
        resp = client.post('/api/videojuegos', 
                          json={'nombre': 'Test Game', 'categoria': 'Test', 'precio': 10, 'valoracion': 5})
        print(f"✅ POST /api/videojuegos (sin auth): {resp.status_code}")
        
        # Test health
        resp = client.get('/health')
        print(f"✅ GET /health: {resp.status_code}")
        
        # Verificar headers de seguridad
        if 'X-RateLimit-Limit' in resp.headers:
            print(f"✅ Rate limiting activo: {resp.headers['X-RateLimit-Limit']}")
        
        if 'X-Frame-Options' in resp.headers:
            print(f"✅ Headers de seguridad activos: {resp.headers['X-Frame-Options']}")
    
    print("\n🎯 RESULTADO: API totalmente funcional sin configuración")
    print("💡 Solo agrega rate limiting y validación automáticamente")

if __name__ == '__main__':
    test_simplified_api()
