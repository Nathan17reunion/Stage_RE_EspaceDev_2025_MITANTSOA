import geopandas as gpd
import os
from collections import defaultdict

# Chemin du dossier contenant les fichiers
#folder_path = r"D:\TDC\Fusion\Par_Site"
#folder_path = r"D:\Manoa\shorelines cleaned"
folder_path = r"D:\Manoa\Court_terme_TDC_01"

# Dictionnaire pour stocker le nombre unique de traits de côte par fichier
results = {}

# Parcourir tous les fichiers avec suffixe _fusion.geojson (Avant filtre) et .geojson (Après filtre)
for filename in os.listdir(folder_path):
    if filename.endswith(".geojson"):
        file_path = os.path.join(folder_path, filename)
        # Charger le fichier GeoJSON
        gdf = gpd.read_file(file_path)
        if "DATE" in gdf.columns:
            # Extraire les dates uniques
            unique_dates = gdf["DATE"].unique()
            # Le nombre de traits de côte est le nombre de dates uniques
            num_traits = len(unique_dates)
            results[filename] = num_traits
        else:
            results[filename] = "Attribut 'DATE' non trouvé"

# Afficher les résultats
for file, count in results.items():
    print(f"{file}: {count} traits de côte uniques (basé sur 'DATE')")
