import geopandas as gpd
import pandas as pd
from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculer_saison(date_val):
    """
    Convertit une date en label saison : 'cyclonique', 'estivale' ou 'autre'.

    - Saison cyclonique : 15/11/année N au 30/04/année N+1
    - Saison estivale : 01/05/année N au 14/11/année N
    """
    if pd.isna(date_val):
        return None

    if not isinstance(date_val, (pd.Timestamp, datetime)):
        try:
            date_val = pd.to_datetime(date_val)
        except Exception:
            logger.debug(f"Impossible de convertir la date '{date_val}'.")
            return None

    year = date_val.year
    month = date_val.month
    day = date_val.day

    # Gestion des chevauchements d'années pour la saison cyclonique (décembre à avril)
    # Si la date est en janvier-avril, l'année de référence pour la saison cyclonique est l'année précédente
    if (month >= 5 and month <= 10) or (month == 11 and day <= 14):
        # Saison estivale du 1er mai au 31 octobre (année N)
        saison_estivale_start = datetime(year, 5, 1)
        saison_estivale_end = datetime(year, 11, 14)
        if saison_estivale_start <= date_val <= saison_estivale_end:
            return "estivale"
        else:
            return "autre"  # en théorie ne devrait pas arriver ici
    else:
        # Saison cyclonique : du 15 novembre (année N) au 30 avril (année N+1)
        if month == 11 or month == 12:
            annee_ref = year
        else:  # mois janvier à avril
            annee_ref = year - 1

        saison_cyclonique_start = datetime(annee_ref, 11, 15)
        saison_cyclonique_end = datetime(annee_ref + 1, 4, 30)

        if saison_cyclonique_start <= date_val <= saison_cyclonique_end:
            return "cyclonique"
        else:
            return "autre"

def ajouter_attribut_saison(gdf):
    """
    Ajoute une colonne 'Saison' à un GeoDataFrame basée sur la colonne 'DATE'.
    Utilise la fonction séparée 'calculer_saison' pour déterminer la saison de chaque date.
    """
    if 'DATE' not in gdf.columns:
        logger.warning("La colonne 'DATE' est absente. Impossible d'ajouter l'attribut 'Saison'.")
        return gdf

    gdf['Saison'] = gdf['DATE'].apply(calculer_saison)
    logger.info("Attribut 'Saison' ajouté basé sur la colonne 'DATE'.")
    return gdf

def traiter_fichier(input_path, output_dir):
    filename = os.path.basename(input_path)
    name_without_ext = os.path.splitext(filename)[0]

    logger.info(f"Traitement du fichier : {filename}")
    gdf = gpd.read_file(input_path)

    # Ajout colonne Saison
    gdf = ajouter_attribut_saison(gdf)

    output_cyclonique = os.path.join(output_dir, f"{name_without_ext}.geojson")
    gdf.to_file(output_cyclonique, driver='GeoJSON')
    logger.info(f"Fichier cyclonique sauvegardé : {output_cyclonique}")

    # Filtrer et sauvegarder cyclonique
    gdf_cyclonique = gdf[gdf['Saison'] == 'cyclonique']
    output_cyclonique = os.path.join(output_dir, f"{name_without_ext}_cyclonique.geojson")
    gdf_cyclonique.to_file(output_cyclonique, driver='GeoJSON')
    logger.info(f"Fichier cyclonique sauvegardé : {output_cyclonique}")

    # Filtrer et sauvegarder estivale
    gdf_estivale = gdf[gdf['Saison'] == 'estivale']
    output_estivale = os.path.join(output_dir, f"{name_without_ext}_estivale.geojson")
    gdf_estivale.to_file(output_estivale, driver='GeoJSON')
    logger.info(f"Fichier estivale sauvegardé : {output_estivale}")

    # Définir la liste des intervalles interannuels (borne inférieure incluse, borne supérieure exclue)
    date_intervalles = [
        ("2015-06-26", "2017-06-28"),
        ("2017-06-28", "2018-06-29"),
        ("2018-06-29", "2019-06-30"),
        ("2019-06-30", "2020-07-01"),
        ("2020-07-01", "2021-07-02"),
        ("2021-07-02", "2022-07-03"),
        ("2022-07-03", "2023-07-04"),
        ("2023-07-04", "2024-07-05"),
        ("2024-07-05", "2025-07-06"),
    ]

    # Convertir chaînes en datetime
    date_intervalles = [(pd.to_datetime(start), pd.to_datetime(end)) for start, end in date_intervalles]

    # Boucle sur chaque intervalle pour filtrer et sauvegarder
    for i, (start_date, end_date) in enumerate(date_intervalles, start=1):
        gdf_intervalle = gdf[(gdf['DATE'] >= start_date) & (gdf['DATE'] < end_date)]

        if gdf_intervalle.empty:
            logger.info(f"Aucune donnée pour l'intervalle {start_date.date()} - {end_date.date()} dans {filename}")
            continue

        # Sauvegarde fichier complet par intervalle (toutes saisons)
        output_path = os.path.join(output_dir, f"{name_without_ext}_interannuel_{i}_{start_date.date()}_{end_date.date()}.geojson")
        gdf_intervalle.to_file(output_path, driver='GeoJSON')
        logger.info(f"Fichier interannuel sauvegardé: {output_path}")

def main():
    input_dir = "/media/jonathan/Expansion/Manoa/shorelines cleaned/"
    output_dir = "/media/jonathan/Expansion/Manoa/Court_terme/"

    os.makedirs(output_dir, exist_ok=True)

    fichiers_a_traiter = ["lhermitage.geojson", "st_denis.geojson", "st_paul.geojson"]

    for f in fichiers_a_traiter:
        input_path = os.path.join(input_dir, f)
        if os.path.isfile(input_path):
            traiter_fichier(input_path, output_dir)
        else:
            logger.warning(f"Fichier non trouvé : {input_path}")

if __name__ == "__main__":
    main()
