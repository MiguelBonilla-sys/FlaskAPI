"""
Script para probar los logs de sincronización.
"""
import requests

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("PROBANDO SYNC LOGS")
print("=" * 60)

# 1. Importar un juego para generar un log
print("\n1. Importando un juego para generar log...")
response = requests.post(
    f"{BASE_URL}/api/videojuegos/importar-externa",
    json={"external_id": "1030"},
    headers={'Content-Type': 'application/json'}
)

if response.status_code == 201:
    data = response.json()
    game = data.get('data', {})
    print(f"✅ Juego importado: {game.get('nombre')} (ID: {game.get('id')})")
else:
    print(f"⚠️  Status: {response.status_code}")

# 2. Ver logs recientes
print("\n2. Consultando logs de sincronización recientes...")
response = requests.get(f"{BASE_URL}/api/sync-logs/recent?limit=10")

if response.status_code == 200:
    data = response.json()
    logs = data.get('data', [])
    print(f"✅ Total de logs encontrados: {len(logs)}")
    
    if logs:
        print("\n📋 Logs de sincronización:")
        for i, log in enumerate(logs[:10], 1):
            status_icon = "✅" if log.get('status') == 'success' else "❌" if log.get('status') == 'failed' else "⏳"
            duration = log.get('duration_seconds', 0)
            print(f"   {i}. {status_icon} External ID: {log.get('external_id')} | "
                  f"Status: {log.get('status')} | "
                  f"Duration: {duration:.2f}s | "
                  f"Videojuego ID: {log.get('videojuego_id', 'N/A')}")
    else:
        print("   ⚠️  No hay logs de sincronización")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

# 3. Ver estadísticas
print("\n3. Consultando estadísticas de sincronización...")
response = requests.get(f"{BASE_URL}/api/sync-logs/statistics?days=7")

if response.status_code == 200:
    data = response.json()
    stats = data.get('data', {})
    print(f"✅ Estadísticas (últimos 7 días):")
    print(f"   Total: {stats.get('total', 0)}")
    print(f"   Exitosos: {stats.get('successful', 0)}")
    print(f"   Fallidos: {stats.get('failed', 0)}")
    print(f"   Pendientes: {stats.get('pending', 0)}")
    print(f"   Tasa de éxito: {stats.get('success_rate', 0):.1f}%")
else:
    print(f"❌ Error: {response.status_code}")

# 4. Ver todos los logs con paginación
print("\n4. Consultando todos los logs (paginados)...")
response = requests.get(f"{BASE_URL}/api/sync-logs?page=1&per_page=5")

if response.status_code == 200:
    data = response.json()
    total = data.get('count', 0)
    logs = data.get('data', [])
    print(f"✅ Total de logs: {total}")
    print(f"   Mostrando: {len(logs)}")
    
    if logs:
        print("\n📋 Primeros logs:")
        for i, log in enumerate(logs, 1):
            status_icon = "✅" if log.get('status') == 'success' else "❌" if log.get('status') == 'failed' else "⏳"
            print(f"   {i}. {status_icon} ID: {log.get('id')} | "
                  f"External ID: {log.get('external_id')} | "
                  f"Status: {log.get('status')}")

print("\n" + "=" * 60)

