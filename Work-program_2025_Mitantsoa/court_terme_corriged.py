import geopandas as gpd
import os
import pandas as pd

# Chemin vers le dossier contenant les fichiers GeoJSON
folder_path = r"D:\Manoa\Interannuel\L'Hermitage"

# Liste pour stocker les GeoDataFrames
layers = []

# Parcourir tous les fichiers dans le dossier
for file in os.listdir(folder_path):
    if file.endswith('.geojson') and file.startswith('rates_lhermitage_'):
        file_path = os.path.join(folder_path, file)
        print(f"Lecture de : {file_path}")
        gdf = gpd.read_file(file_path)
        layers.append(gdf)

if layers:
    # Fusionner tous les GeoDataFrames
    merged_gdf = gpd.GeoDataFrame(pd.concat(layers, ignore_index=True), crs=layers[0].crs)
    
    # Chemin de sortie
    output_path = os.path.join(folder_path, 'rates_lhermitage_fused.geojson')
    
    # Sauvegarder le fichier fusionné
    merged_gdf.to_file(output_path, driver='GeoJSON')
    print(f"Fichier fusionné sauvegardé ici : {output_path}")
else:
    print("Aucun fichier correspondant trouvé dans le dossier.")
