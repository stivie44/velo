import requests

# Clé API pour l'API JCDecaux
api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"

# Ville pour laquelle nous souhaitons récupérer les données de la station de vélos
city = "creteil"

# URL de l'API pour la ville sélectionnée
url = f"https://api.jcdecaux.com/vls/v1/stations?contract={city}&apiKey={api_key}"

# Récupérer les données de l'API
response = requests.get(url)
data = response.json()

# Calculer le nombre total de vélos mécaniques et électriques
mechanical_bikes = 0
electric_bikes = 0
for station in data:
    try:
        mechanical_bikes += station["mainStands"]["mechanical"]
        electric_bikes += station["mainStands"]["electrical"]
    except KeyError:
        # Si la clé "mainStands" est absente, ignorez cette station de vélos
        pass

# Calculer le pourcentage de vélos mécaniques et électriques
total_bikes = mechanical_bikes + electric_bikes
if total_bikes > 0:
    mechanical_bikes_percentage = mechanical_bikes / total_bikes * 100
    electric_bikes_percentage = electric_bikes / total_bikes * 100
else:
    mechanical_bikes_percentage = 0
    electric_bikes_percentage = 0

# Afficher les résultats
print(f"Pourcentage de vélos mécaniques à {city}: {mechanical_bikes_percentage:.2f}%")
print(f"Pourcentage de vélos électriques à {city}: {electric_bikes_percentage:.2f}%")

# Trier les stations de vélos par nombre de vélos disponibles
sorted_stations = sorted(data, key=lambda x: x["available_bikes"], reverse=True)

# Afficher les 5 premières stations de vélos
print(f"\nLes 5 premières stations de vélos à {city} par nombre de vélos disponibles:")
for i in range(5):
    station = sorted_stations[i]
    print(f"{i+1}. {station['name']} - {station['available_bikes']} vélos disponibles")
