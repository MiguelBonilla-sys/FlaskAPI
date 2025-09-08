"""
Script de prueba para verificar las medidas de seguridad implementadas.
"""
import requests
import time
import json

# Configuración
BASE_URL = "http://localhost:5000"
API_KEYS = {
    'admin': 'admin_secure_key_2025_videogames_api',
    'writer': 'writer_key_2025_content_manager',
    'readonly': 'readonly_key_2025_public_access'
}

def test_rate_limiting():
    """
    Prueba el rate limiting.
    """
    print("🔥 Probando Rate Limiting...")
    
    # Hacer muchas peticiones rápidas para activar el rate limiting
    for i in range(65):  # Más del límite de 60 por minuto
        try:
            response = requests.get(f"{BASE_URL}/api/videojuegos", timeout=2)
            if response.status_code == 429:
                print(f"✅ Rate limiting activado en petición #{i+1}")
                print(f"   Headers: {dict(response.headers)}")
                break
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en petición #{i+1}: {e}")
            break
    else:
        print("⚠️  Rate limiting no se activó (puede estar en modo debug)")

def test_authentication():
    """
    Prueba la autenticación con API keys.
    """
    print("\n🔐 Probando Autenticación...")
    
    # Test sin API key (debería fallar en endpoints protegidos)
    try:
        response = requests.post(f"{BASE_URL}/api/videojuegos", 
                               json={'nombre': 'Test Game', 'categoria': 'Test', 'precio': 10, 'valoracion': 5},
                               timeout=5)
        if response.status_code == 401:
            print("✅ Endpoints protegidos requieren autenticación")
        else:
            print(f"⚠️  Endpoint desprotegido: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test con API key inválida
    try:
        headers = {'X-API-Key': 'invalid_key'}
        response = requests.post(f"{BASE_URL}/api/videojuegos",
                               json={'nombre': 'Test Game', 'categoria': 'Test', 'precio': 10, 'valoracion': 5},
                               headers=headers, timeout=5)
        if response.status_code == 401:
            print("✅ API key inválida rechazada correctamente")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test con API key válida pero permisos insuficientes
    try:
        headers = {'X-API-Key': API_KEYS['readonly']}
        response = requests.post(f"{BASE_URL}/api/videojuegos",
                               json={'nombre': 'Test Game', 'categoria': 'Test', 'precio': 10, 'valoracion': 5},
                               headers=headers, timeout=5)
        if response.status_code == 403:
            print("✅ Permisos insuficientes detectados correctamente")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def test_input_validation():
    """
    Prueba la validación de entrada.
    """
    print("\n🛡️  Probando Validación de Entrada...")
    
    # Test con datos maliciosos (SQL injection)
    malicious_data = {
        'nombre': "'; DROP TABLE videojuegos; --",
        'categoria': 'Test',
        'precio': 10,
        'valoracion': 5
    }
    
    try:
        headers = {'X-API-Key': API_KEYS['writer']}
        response = requests.post(f"{BASE_URL}/api/videojuegos",
                               json=malicious_data,
                               headers=headers, timeout=5)
        if response.status_code == 400:
            print("✅ Intento de SQL injection bloqueado")
            if response.headers.get('content-type', '').startswith('application/json'):
                data = response.json()
                print(f"   Errores: {data.get('errors', [])}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    
    # Test con datos XSS
    xss_data = {
        'nombre': '<script>alert("XSS")</script>',
        'categoria': 'Test',
        'precio': 10,
        'valoracion': 5
    }
    
    try:
        headers = {'X-API-Key': API_KEYS['writer']}
        response = requests.post(f"{BASE_URL}/api/videojuegos",
                               json=xss_data,
                               headers=headers, timeout=5)
        if response.status_code == 400:
            print("✅ Intento de XSS bloqueado")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def test_endpoints_public():
    """
    Prueba endpoints públicos.
    """
    print("\n🌐 Probando Endpoints Públicos...")
    
    public_endpoints = [
        '/health',
        '/api/',
        '/api/videojuegos',
        '/api/videojuegos/categorias'
    ]
    
    for endpoint in public_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint} - Accesible públicamente")
            else:
                print(f"❌ {endpoint} - Error {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error de conexión: {e}")

def test_security_headers():
    """
    Prueba los headers de seguridad.
    """
    print("\n🔒 Probando Headers de Seguridad...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        security_headers = [
            'X-Frame-Options',
            'X-Content-Type-Options', 
            'X-XSS-Protection',
            'Content-Security-Policy',
            'X-RateLimit-Limit'
        ]
        
        for header in security_headers:
            if header in response.headers:
                print(f"✅ {header}: {response.headers[header]}")
            else:
                print(f"❌ {header}: No presente")
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def main():
    """
    Función principal de pruebas de seguridad.
    """
    print("🎮 PRUEBAS DE SEGURIDAD - API de Videojuegos")
    print("=" * 50)
    
    # Verificar si el servidor está corriendo
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor está corriendo\n")
        else:
            print(f"❌ Servidor respondió con código {response.status_code}\n")
            return
    except requests.exceptions.RequestException:
        print("❌ No se pudo conectar al servidor")
        print("   Asegúrate de que la aplicación esté corriendo en http://localhost:5000")
        return
    
    # Ejecutar pruebas
    test_endpoints_public()
    test_security_headers()
    test_authentication()
    test_input_validation()
    test_rate_limiting()
    
    print("\n" + "=" * 50)
    print("🎯 Pruebas de seguridad completadas")
    print("\n📋 Para pruebas manuales adicionales:")
    print("1. Intenta acceder a endpoints protegidos sin API key")
    print("2. Usa herramientas como Postman para probar límites de rate")
    print("3. Verifica logs de la aplicación para alertas de seguridad")

if __name__ == '__main__':
    main()
