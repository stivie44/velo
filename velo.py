import requests

# Liste des villes disponibles
villes = ["Bruxelles","Amiens", "Lyon","Marseille","Rouen", "Nantes", "Toulouse","Namur","Santander","Toyama,","Vilnius"]

# Affichage de la liste des villes
print("Villes disponibles :")
for ville in villes:
    print("- " + ville)

# Demande à l'utilisateur de choisir une ville
ville_choisie = input("Choisissez une ville dans la liste : ")

# Vérification de la validité de la ville choisie
while ville_choisie not in villes:
    print("Ville invalide.")
    ville_choisie = input("Choisissez une ville dans la liste : ")

# Récupération des données de la ville choisie depuis l'API JCDecaux
api_key = "e0a1bf2c844edb9084efc764c089dd748676cc14"
url = f"https://api.jcdecaux.com/vls/v3/stations?contract={ville_choisie}&apiKey={api_key}"
response = requests.get(url)

# Traitement des données si la requête a abouti
if response.status_code == 200:
    data = response.json()

    # trier les stations par pourcentage de vélos disponibles
    sorted_stations = sorted(data, key=lambda x: x["totalStands"]["availabilities"]["bikes"] / x["totalStands"]["capacity"], reverse=True)

    
    # afficher les 5 premières stations avec leur pourcentage de vélos disponibles, de vélos électriques et de vélos mécaniques
    for station in sorted_stations[:5]:
        available_bike = station["totalStands"]["availabilities"]["bikes"]
        capacity = station["totalStands"]["capacity"]
        percentage = int(available_bike / capacity * 100)
        electric_bikes = station["totalStands"]["availabilities"].get("bikesElectrical", 0)
        mechanical_bikes = available_bike - electric_bikes
        electric_percentage = int(electric_bikes / capacity * 100)
        mechanical_percentage = int(mechanical_bikes / capacity * 100)
        print(f"{station['name']} - {percentage}% de vélos disponibles ({available_bike}/{capacity} vélos) dont {electric_percentage}% électriques ({electric_bikes}/{capacity} vélos) et {mechanical_percentage}% mécaniques ({mechanical_bikes}/{capacity} vélos)")

# Affichage d'un message d'erreur si la requête a échoué
else:
    print("Erreur lors de la récupération des données.")
