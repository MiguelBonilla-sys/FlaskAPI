"""
Script para ejecutar todos los tests de endpoints.
"""
import os
import sys
import subprocess

def run_tests():
    """Ejecuta todos los tests de endpoints."""
    print("=" * 60)
    print("TESTS DE ENDPOINTS - EJECUTANDO")
    print("=" * 60)
    
    # Cambiar al directorio del proyecto
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    # Ejecutar tests
    result = subprocess.run(
        ["python", "-m", "pytest", "Test/test_all_endpoints.py", "-v", "--tb=short"],
        capture_output=False,
        text=True
    )
    
    print("\n" + "=" * 60)
    if result.returncode == 0:
        print("SUCCESS: TODOS LOS TESTS DE ENDPOINTS PASARON")
    else:
        print("ERROR: ALGUNOS TESTS FALLARON")
    print("=" * 60)
    
    return result.returncode == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

