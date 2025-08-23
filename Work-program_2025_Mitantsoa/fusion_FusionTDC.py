import os
import geopandas as gpd
import pandas as pd

# ... (partie fusion des dossiers inchangée)

dossiers = [
    "/media/jonathan/Expansion/TDC/Fusion/AWEINSH/",
    "/media/jonathan/Expansion/TDC/Fusion/AWEISH/",
    "/media/jonathan/Expansion/TDC/Fusion/MNDWI/",
    "/media/jonathan/Expansion/TDC/Fusion/NDWI/"
]
chemin_sortie = "/media/jonathan/Expansion/TDC/Fusion/"
nom_commun = "fusion_trait_de_cote"

fichiers_fusionnes = []

for dossier in dossiers:
    fichiers = [
        f for f in os.listdir(dossier)
        if f.endswith('_Corriger.shp')
    ]
    liste_gdf = []
    for f in fichiers:
        gdf = gpd.read_file(os.path.join(dossier, f))
        liste_gdf.append(gdf)
    if liste_gdf:
        gdf_total = pd.concat(liste_gdf, ignore_index=True)
        nom_fusion = os.path.basename(os.path.normpath(dossier)) + "_Fusion.shp"
        chemin_fusion = os.path.join(chemin_sortie, nom_fusion)
        gdf_total.to_file(chemin_fusion)
        fichiers_fusionnes.append(chemin_fusion)


# Fusion finale des 4 shapefiles
liste_gdf_final = [gpd.read_file(f) for f in fichiers_fusionnes]
if liste_gdf_final:
    gdf_final = pd.concat(liste_gdf_final, ignore_index=True)
    chemin_fusion_finale = os.path.join(chemin_sortie, "fusion_trait_de_cote_tous.shp")
    gdf_final.to_file(chemin_fusion_finale)

# Chemin vers le shapefile global fusionné
chemin_fusion_tous = "/media/jonathan/Expansion/TDC/Fusion/fusion_trait_de_cote_tous.shp"

# Dossier de sortie pour les shapefiles par site
output_sites_dir = "/media/jonathan/Expansion/TDC/Fusion/Par_Site/"
os.makedirs(output_sites_dir, exist_ok=True)

# Dossier de sortie pour les shapefiles et GeoJSON par cellule hydrosédimentaire
output_dir = "/media/jonathan/Expansion/TDC/Fusion/Par_Cellule_Hydrosedimentaire/"
os.makedirs(output_dir, exist_ok=True)

# Chargement du shapefile global
gdf_fusion = gpd.read_file(chemin_fusion_tous)

# Vérification de la présence de la colonne 'BEACH_CODE'
if 'BEACH_CODE' not in gdf_fusion.columns:
    raise KeyError("La colonne 'BEACH_CODE' est absente du GeoDataFrame fusionné.")

# Dictionnaire des types de cellules hydrosédimentaires avec leurs codes BEACH_CODE
cellules_hydrosedimentaires = {
    "Plage_Sable_Blanc_Sans_Recif": [8212,8213,8214,8281],
    "Plage_Sable_Blanc_Avec_Recif": [8192,8194,8195,8196,8197,8198,8199,8200,8201,8202,8203,8204,8205,8206,8207,8208,8209,8210,8211,8215,8216,8217,8221,8222,8223,8234,8280],
    "Plage_Sable_Noir_Avec_Recif": [8225,8226],
    "Plage_Sable_Noir_Sans_Recif": [8224,8267,8271,8272,8277,8278,8279],
    "Plage_Mixte_Sans_Recif": [8232,8268,8269,8270,8273,8275,8276,8283],
    "Plage_Mixte_Avec_Recif": [8193,8218,8219,8220,8227],
    "Plage_Galets": [8228,8230,8231,8235,8237,8238,8239,8240,8241,8242,8243,8244,8245,8246,8247,8248,8249,8250,8251,8253,8254,8255,8256,8257,8258,8259,8260,8262,8263,8265],
    "Embouchure_Delta": [8223,8229,8236,8252,8261,8264,8266,8274,8282]
}

for cellule_name, codes in cellules_hydrosedimentaires.items():
    print(f"Extraction pour la cellule hydrosédimentaire : {cellule_name}")

    # Filtrer les entités correspondant aux codes BEACH_CODE de la cellule
    gdf_cellule = gdf_fusion[gdf_fusion['BEACH_CODE'].isin(codes)].copy()

    if gdf_cellule.empty:
        print(f"Aucun trait de côte trouvé pour la cellule {cellule_name}.")
        continue

    # Optionnel : fusionner les géométries par site (décommenter si besoin)
    #gdf_cellule = gdf_cellule.dissolve(by='BEACH_CODE')

    # Sauvegarder en shapefile
    shp_path = os.path.join(output_dir, f"{cellule_name}.shp")
    gdf_cellule.to_file(shp_path)

    # Sauvegarder en GeoJSON
    geojson_path = os.path.join(output_dir, f"{cellule_name}.geojson")
    gdf_cellule.to_file(geojson_path, driver="GeoJSON")

print(f"Extraction terminée. Fichiers enregistrés dans : {output_dir}")

# Dictionnaire des sites avec leurs beach_codes associés
sites_beach_codes = {
    "Baie_Saint_Paul": [8272,8273,8274,8275,8276,8277,8278,8279],
    "Etang_Sale": [8223,8224,8225,8226,8227,8283],
    "Hermitage_La_Saline": [8201,8202,8203,8204,8205,8206,8207,8208],
    "La_Possession": [8267,8268],
    "Le_Port": [8269,8270,8271],
    "Saint_Benoit": [8235,8236,8237,8238,8239,8240,8241,8242,8243,8244,8245,8246,8247,8248,8249,8250,8251,8252,8253],
    "Saint_Denis": [8261,8262,8263,8264,8265,8266],
    "Saint_Gille": [8192,8193,8194,8195,8196,8197,8198,8199,8200],
    "Saint_Joseph": [8282],
    "Saint_Leu": [8209,8210,8211,8212,8213,8214,8215,8216,8217,8218,8219,8220,8221,8222],
    "Saint_Louis": [8228,8229,8230,8231,8232],
    "Saint_Pierre": [8233,8234,8280,8281],
    "Sainte_Marie": [8258,8259,8260],
    "Sainte_Suzanne": [8254,8255,8256,8257]
}

# Fonction simple d'affichage de progression (optionnelle)
def show_progress(current, total, message=""):
    print(f"[{current}/{total}] {message}")

current_step = 1
total_sites = len(sites_beach_codes)

for site_name, codes in sites_beach_codes.items():
    show_progress(current_step, total_sites, f"Extraction et sauvegarde pour le site : {site_name}")

    # Filtrer les entités correspondant aux beach_codes du site
    gdf_site = gdf_fusion[gdf_fusion['BEACH_CODE'].isin(codes)].copy()

    if gdf_site.empty:
        print(f"Aucun trait de côte trouvé pour le site {site_name}.")
        current_step += 1
        continue

    gdf_site['Site'] = site_name

    # Optionnel : fusionner les géométries par site (décommenter si besoin)
    #gdf_site = gdf_site.dissolve(by='BEACH_CODE')

    # Sauvegarder le shapefile du site
    output_path_site = os.path.join(output_sites_dir, f"{site_name}_fusion.shp")
    gdf_site.to_file(output_path_site)

    # Sauvegarder aussi en GeoJSON
    output_path_geojson = os.path.join(output_sites_dir, f"{site_name}_fusion.geojson")
    gdf_site.to_file(output_path_geojson, driver="GeoJSON")

    current_step += 1

# Fichiers des traits de côte par site
sites_etude = {
    "HermSal": "/media/jonathan/Expansion/TDC/Fusion/Par_Site/Hermitage_La_Saline_fusion.shp",
    "BaieStPaul": "/media/jonathan/Expansion/TDC/Fusion/Par_Site/Baie_Saint_Paul_fusion.shp",
    "StDenis": "/media/jonathan/Expansion/TDC/Fusion/Par_Site/Saint_Denis_fusion.shp"
}

# Chemin du masque (à VÉRIFIER)
mask_path = "/media/jonathan/Expansion/TDC/Mask_Embouchure&Delta.shp"  # Ou corrige si le nom est différent

if not os.path.exists(mask_path):
    raise FileNotFoundError(f"Le fichier masque n'est pas trouvé : {mask_path}")

mask_gdf = gpd.read_file(mask_path)

for site_name, site_path in sites_etude.items():
    print(f"Traitement du masquage pour le site {site_name} ...")

    site_gdf = gpd.read_file(site_path)
    # Harmoniser le système de coordonnées
    if site_gdf.crs != mask_gdf.crs:
        mask_proj = mask_gdf.to_crs(site_gdf.crs)
    else:
        mask_proj = mask_gdf

    # Opération de masque : on retire toutes les embouchures du site étudié
    site_masked = site_gdf.overlay(mask_proj, how='difference')

    # Sauvegarde
    output_shp = os.path.join(output_sites_dir, f"{site_name}_mask.shp")
    site_masked.to_file(output_shp)
    output_geojson = os.path.join(output_sites_dir, f"{site_name}_mask.geojson")
    site_masked.to_file(output_geojson, driver='GeoJSON')

    print(f"Fichiers enregistrés pour {site_name}: {output_shp}, {output_geojson}")

print(f"Extraction par site terminée. Shapefiles sauvegardés dans : {output_sites_dir}")
