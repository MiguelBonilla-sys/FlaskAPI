"""
Verificar el resultado final de la importación.
"""
import requests

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("VERIFICACIÓN FINAL")
print("=" * 60)

# Obtener videojuegos
response = requests.get(f"{BASE_URL}/api/videojuegos")
data = response.json()
total = data.get('count', len(data.get('data', [])))

print(f"\n✅ Total de videojuegos: {total}")

# Obtener desarrolladoras
response = requests.get(f"{BASE_URL}/api/desarrolladoras")
dev_data = response.json()
total_devs = dev_data.get('count', len(dev_data.get('data', [])))
print(f"✅ Total de desarrolladoras: {total_devs}")

print("\n📋 Lista de juegos con desarrolladoras:")
games = data.get('data', [])[:15]
for i, game in enumerate(games, 1):
    dev = game.get('desarrolladora', {})
    dev_name = dev.get('nombre', 'N/A') if dev else game.get('desarrollador', 'N/A')
    print(f"   {i}. {game.get('nombre')} - Dev: {dev_name}")

print("\n🏢 Desarrolladoras creadas:")
for i, dev in enumerate(dev_data.get('data', []), 1):
    print(f"   {i}. {dev.get('nombre')}")

print("\n" + "=" * 60)
if total >= 15:
    print("✅ ¡OBJETIVO CUMPLIDO! Tienes 15 o más juegos importados.")
else:
    print(f"⚠️  Tienes {total} juegos. Faltan {15 - total} para llegar a 15.")
print("=" * 60)

