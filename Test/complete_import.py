"""
Script para completar la importación hasta 15 juegos.
"""
import requests
import json

BASE_URL = "http://localhost:5000"

# Juegos adicionales para llegar a 15
additional_games = [
    {"external_id": "3268", "name": "The Witcher 2"},
    {"external_id": "1030", "name": "Half-Life"},
    {"external_id": "58175", "name": "God of War"},
    {"external_id": "58134", "name": "Red Dead Redemption 2"},
]

print("=" * 60)
print("COMPLETANDO IMPORTACIÓN HASTA 15 JUEGOS")
print("=" * 60)

# Importar juegos adicionales
games_to_import = [{"external_id": game["external_id"]} for game in additional_games]

response = requests.post(
    f"{BASE_URL}/api/videojuegos/importar-batch",
    json={"games": games_to_import},
    headers={'Content-Type': 'application/json'}
)

if response.status_code in [201, 207]:
    data = response.json()
    print(f"\n✅ Importación completada!")
    print(f"   Exitosos: {len(data.get('data', {}).get('success', []))}")
    print(f"   Fallidos: {len(data.get('data', {}).get('failed', []))}")
    print(f"   Omitidos: {len(data.get('data', {}).get('skipped', []))}")
    
    if data.get('data', {}).get('success'):
        print("\n📦 Juegos importados:")
        for game in data['data']['success']:
            dev = game.get('desarrolladora', {})
            dev_name = dev.get('nombre', 'Sin desarrolladora') if dev else game.get('desarrollador', 'Sin desarrolladora')
            print(f"   - {game.get('nombre')} (ID: {game.get('id')}) - Dev: {dev_name}")

# Verificar total
print("\n" + "=" * 60)
print("RESUMEN FINAL")
print("=" * 60)

response = requests.get(f"{BASE_URL}/api/videojuegos")
if response.status_code == 200:
    data = response.json()
    total = data.get('count', len(data.get('data', [])))
    print(f"\n✅ Total de videojuegos: {total}")
    
    print("\n📋 Lista de juegos:")
    for i, game in enumerate(data.get('data', [])[:15], 1):
        dev = game.get('desarrolladora', {})
        dev_name = dev.get('nombre', 'N/A') if dev else game.get('desarrollador', 'N/A')
        print(f"   {i}. {game.get('nombre')} - Dev: {dev_name}")

response = requests.get(f"{BASE_URL}/api/desarrolladoras")
if response.status_code == 200:
    data = response.json()
    total_devs = data.get('count', len(data.get('data', [])))
    print(f"\n✅ Total de desarrolladoras: {total_devs}")
    
    print("\n🏢 Lista de desarrolladoras:")
    for i, dev in enumerate(data.get('data', []), 1):
        print(f"   {i}. {dev.get('nombre')}")

print("\n" + "=" * 60)

