import os
import re
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
from datetime import datetime

# --- Constantes et Fonctions utilitaires ---

epsg_reunion = 2975

def show_progress(current_step, total_steps, message):
    percent = int(100 * current_step / total_steps)
    now = datetime.now().strftime("%d/%m/%Y || %H:%M:%S")
    print(f"{now} || [{percent:3d}%] {message}")

def extract_date_from_filename(filename):
    match = re.search(r'(\d{8})T\d{6}', filename)
    if match:
        return match.group(1)
    else:
        return pd.NA

def attribuer_etat(date):
    if pd.isnull(date):
        return 'NA'
    annee = date.year
    if 2015 <= annee < 2019:
        return 'TDC ancien'
    elif 2019 <= annee < 2022:
        return 'TDC intermédiaire'
    elif 2022 <= annee <= 2025:
        return 'TDC récent'
    else:
        return 'NA'

plages_sable_blanc_sans_recif = [8193, 8212, 8213, 8214, 8281]
plages_sable_blanc_avec_recif = [8192, 8194, 8195, 8196, 8197, 8198, 8199, 8200, 8201, 8202, 8203, 8204, 8205, 8206, 8207, 8208, 8209, 8210, 8211, 8215, 8216, 8217, 8221, 8222, 8233, 8234, 8280]
plages_sable_noir_sans_recif = [8224, 8267, 8271, 8272, 8277, 8278, 8279]
plages_sable_noir_avec_recif = [8225, 8226]
plages_mixtes_sans_recif = [8232, 8268, 8269, 8270, 8273, 8275, 8276, 8283, 8218, 8219, 8220, 8227, 8193]
plages_galets = [8228, 8230, 8231, 8235, 8237, 8238, 8239, 8240, 8241, 8242, 8243, 8244, 8245, 8246, 8247, 8248, 8249, 8250, 8251, 8253, 8254, 8255, 8256, 8257, 8258, 8259, 8260, 8262, 8263, 8265]
embouchures = [8223, 8229, 8236, 8252, 8261, 8264, 8266, 8274, 8282]

def classer_groupe(beach_code):
    if beach_code in plages_sable_blanc_sans_recif:
        return "Plage sable blanc sans récif"
    elif beach_code in plages_sable_blanc_avec_recif:
        return "Plage sable blanc avec récif"
    elif beach_code in plages_sable_noir_sans_recif:
        return "Plage sable noir sans récif"
    elif beach_code in plages_sable_noir_avec_recif:
        return "Plage sable noir avec récif"
    elif beach_code in plages_mixtes_sans_recif:
        return "Plage mixte sans récif"
    elif beach_code in plages_galets:
        return "Plage à galets"
    elif beach_code in embouchures:
        return "Embouchure"
    else:
        return "Autres / non classé"

if __name__ == "__main__":
    dossier_base = "/home/jonathan/SAET/SAET_installation/SAET_master/output_data/sds/"
    chemin_terre = "/home/jonathan/SAET/SAET_installation/SAET_master/aux_data/beaches.shp"
    output_dir = "/home/jonathan/Images/Fusion/"
    os.makedirs(output_dir, exist_ok=True)

    total_steps = 3
    current_step = 1

    terre = gpd.read_file(chemin_terre)
    terre = terre.to_crs(epsg=epsg_reunion)

    show_progress(current_step, total_steps, "Chargement et traitement des traits de côtes...")
    all_gdfs = []
    for root, dirs, files in os.walk(dossier_base):
        for fichier in files:
            if fichier.endswith('_lines.shp'):
                chemin_shp = os.path.join(root, fichier)
                print(f"Chargement du shapefile : {chemin_shp}")
                gdf = gpd.read_file(chemin_shp)
                if len(gdf) == 0:
                    print(f"Attention : fichier {fichier} vide.")
                    continue
                gdf = gdf.to_crs(epsg=epsg_reunion)
                date_extrait = extract_date_from_filename(fichier)
                date_extrait_dt = pd.to_datetime(date_extrait, format='%Y%m%d', errors='coerce')
                if 'OBJECTED' not in gdf.columns:
                    gdf['OBJECTED'] = range(1, len(gdf) + 1)
                gdf['SHAPE'] = gdf.geometry.geom_type
                gdf['SHAPE_length'] = gdf.geometry.length
                gdf['DATE'] = gdf['DATE'].fillna(date_extrait_dt) if 'DATE' in gdf.columns else date_extrait_dt
                gdf['UNCERTAINTY'] = gdf.get('UNCERTAINTY', pd.NA)
                all_gdfs.append(gdf)

    if not all_gdfs:
        raise FileNotFoundError("Aucun trait de côte trouvé. Vérifiez les chemins et les fichiers.")
    current_step += 1

    show_progress(current_step, total_steps, "Fusion des GeoDataFrames des traits de côtes...")
    gdf_fusion = gpd.GeoDataFrame(pd.concat(all_gdfs, ignore_index=True), crs=f"EPSG:{epsg_reunion}")
    gdf_fusion['DATE'] = pd.to_datetime(gdf_fusion['DATE'], errors='coerce')
    current_step += 1

    gdf_fusion['annee'] = gdf_fusion['DATE'].dt.year
    gdf_fusion['etat'] = gdf_fusion['DATE'].apply(attribuer_etat)

    beach_codes_series = gdf_fusion.get('BEACH_CODE')
    if beach_codes_series is not None:
        gdf_fusion['GROUP'] = beach_codes_series.apply(classer_groupe)
    else:
        print("La colonne 'BEACH_CODE' est absente. La colonne 'GROUP' sera initialisée à 0.")
        gdf_fusion['GROUP'] = 0

    output_path = os.path.join(output_dir, "fusion_trait_de_cote.shp")
    gdf_fusion.to_file(output_path)
    print(f"GeoDataFrame fusionné sauvegardé dans : {output_path}")


















