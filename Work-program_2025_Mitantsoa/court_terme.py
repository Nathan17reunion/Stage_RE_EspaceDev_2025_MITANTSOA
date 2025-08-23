import geopandas as gpd

# Chemins des fichiers
fichier_input = r'D:\\Manoa\\Results DSAS\\merged_rates_all_sites.geojson'
fichier_output = r'D:\\Manoa\\Results DSAS\\merged_rates_all_sites_tendance.geojson'

# Charger le fichier GeoJSON
geo_df = gpd.read_file(fichier_input)

# Fonction pour créer l'attribut 'Tendances' selon 'EPR'
def tendance_epr(epr):
    if epr < 0:
        return 'Erosion'
    elif epr > 0:
        return 'Accrétion'
    else:
        return None  # EPR = 0 ignoré

# Appliquer la fonction sur l'attribut 'EPR'
geo_df['Tendances'] = geo_df['EPR'].apply(tendance_epr)

# Enregistrer le fichier modifié
geo_df.to_file(fichier_output, driver='GeoJSON')

print(f"Fichier enregistré sous : {fichier_output}")
