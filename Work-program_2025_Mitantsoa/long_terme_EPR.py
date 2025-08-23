import geopandas as gpd
from pathlib import Path
import pandas as pd

# Chemin du dossier principal (à adapter selon votre environnement)
root_folder = Path('/media/jonathan/Expansion/Manoa/Results DSAS/')

all_gdfs = []

# Parcours des sous-dossiers (sites)
for site_folder in root_folder.iterdir():
    if site_folder.is_dir():
        # Recherche des fichiers commençant par 'rates_' et finissant par '.geojson'
        geojson_files = list(site_folder.glob('rates_*.geojson'))
        for file_path in geojson_files:
            try:
                gdf = gpd.read_file(file_path)
                all_gdfs.append(gdf)
            except Exception as e:
                print(f"Erreur à la lecture de {file_path} : {e}")

# Fusion de tous les GeoDataFrames si la liste n’est pas vide
if all_gdfs:
    merged_gdf = gpd.GeoDataFrame(pd.concat(all_gdfs, ignore_index=True))
    output_path = root_folder / 'merged_rates_all_sites.geojson'
    merged_gdf.to_file(output_path, driver='GeoJSON')
    print(f"Fichier fusionné sauvegardé sous : {output_path}")
else:
    print("Aucun fichier valide trouvé pour la fusion.")
