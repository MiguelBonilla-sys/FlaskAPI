"""
Script maestro para ejecutar todos los tests del proyecto.
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado."""
    print("\n" + "=" * 60)
    print(f"🧪 {description}")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False

def main():
    """Ejecuta todos los tests."""
    print("=" * 60)
    print("🚀 EJECUTANDO TODOS LOS TESTS")
    print("=" * 60)
    
    # Cambiar al directorio del proyecto
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    results = {}
    
    # 1. Tests unitarios (no requieren servidor)
    print("\n📋 FASE 1: Tests Unitarios (no requieren servidor)")
    results['unit'] = run_command(
        "python Test/test_services.py",
        "Tests Unitarios de Servicios"
    )
    
    # 2. Tests de endpoints básicos (requieren servidor)
    print("\n📋 FASE 2: Tests de Endpoints (requieren servidor corriendo)")
    print("⚠️  Asegúrate de que el servidor Flask esté corriendo en http://localhost:5000")
    input("Presiona Enter para continuar o Ctrl+C para cancelar...")
    
    results['endpoints'] = run_command(
        "python Test/test_videojuegos_endpoints.py",
        "Tests de Endpoints Básicos"
    )
    
    # 3. Tests de integración RAWG (requieren servidor y API key)
    print("\n📋 FASE 3: Tests de Integración RAWG (requieren servidor y API key)")
    print("⚠️  Requiere: Servidor Flask + RAWG_API_KEY configurada")
    input("Presiona Enter para continuar o Ctrl+C para cancelar...")
    
    results['rawg'] = run_command(
        "python Test/test_rawg_integration.py",
        "Tests de Integración RAWG API"
    )
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"✅ Tests pasados: {passed}/{total}")
    print(f"❌ Tests fallidos: {total - passed}/{total}")
    
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"   {status} {test_name}")
    
    print("\n💡 Para ejecutar tests individuales:")
    print("   - Unitarios: python Test/test_services.py")
    print("   - Endpoints: python Test/test_videojuegos_endpoints.py")
    print("   - RAWG: python Test/test_rawg_integration.py")
    print("   - Con pytest: pytest Test/ -v")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

