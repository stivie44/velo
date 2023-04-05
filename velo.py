import requests

# Définition de l'API key
api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"

villes = ["Bruxelles","Amiens", "Lyon","Marseille","Rouen", "Nantes", "Toulouse","Namur","Santander","Toyama,","Vilnius"]

# Récupération des données de toutes les villes depuis l'API JCDecaux
villes_data = []
for ville in villes:
    url = f"https://api.jcdecaux.com/vls/v3/stations?contract={ville}&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        villes_data.append({"ville": ville, "total_bikes": sum([station['totalStands']['availabilities']['bikes'] for station in data])})

# Tri de la liste des villes par rapport au nombre total de vélos disponibles
villes_data = sorted(villes_data, key=lambda x: x["total_bikes"], reverse=True)

# Affichage de la liste des villes triée par rapport au nombre de vélos disponibles
print("Villes triées par rapport au nombre total de vélos disponibles :")
for i, ville_data in enumerate(villes_data):
    print(f"{i+1}. {ville_data['ville']} ({ville_data['total_bikes']} vélos)")

# Demande à l'utilisateur de choisir une ville
ville_choisie = input("Choisissez une ville dans la liste : ")

# Vérification de la validité de la ville choisie
while ville_choisie not in villes:
    print("Ville invalide.")
    ville_choisie = input("Choisissez une ville dans la liste : ")

# Récupération des données de la ville choisie depuis l'API JCDecaux
url = f"https://api.jcdecaux.com/vls/v3/stations?contract={ville_choisie}&apiKey={api_key}"
response = requests.get(url)

# Traitement des données si la requête a abouti
if response.status_code == 200:
    data = response.json()

    # trier les stations par pourcentage de vélos disponibles
    sorted_stations = sorted(data, key=lambda x: x["totalStands"]["availabilities"]["bikes"] / x["totalStands"]["capacity"], reverse=True)

    # afficher les 5 premières stations avec leur pourcentage de vélos disponibles
    print(f"Les 5 stations avec le plus grand pourcentage de vélos disponibles à {ville_choisie} :")
    for station in sorted_stations[:5]:
        available_bike = station["totalStands"]["availabilities"]["bikes"]
        if "bikesElectrical" in station["totalStands"]["availabilities"]:
            electric_bikes = station["totalStands"]["availabilities"]["bikesElectrical"]
        else:
            electric_bikes = 0
        mechanical_bikes = available_bike - electric_bikes
        capacity = station["totalStands"]["capacity"]
        percentage = int(available_bike / capacity * 100)
        print(f"{station['name']} - {percentage}% de vélos disponibles ({available_bike}/{capacity} vélos, dont {electric_bikes} électriques et {mechanical_bikes} mécaniques)")

# Affichage d'un message d'erreur si la requête a échoué
else:
    print("Erreur lors de la récupération des données.")

