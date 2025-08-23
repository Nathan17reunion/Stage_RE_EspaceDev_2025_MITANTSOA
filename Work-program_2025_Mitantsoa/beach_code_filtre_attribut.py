import geopandas as gpd

# Chargement du shapefile
path_beaches = "/home/jonathan/SAET/SAET_installation/SAET_master/aux_data/beaches.shp"
gdf = gpd.read_file(path_beaches)

# Filtrer sur les codes pour Réunion uniquement (8192 à 8283)
gdf = gdf[(gdf['BEACH_CODE'] >= 8192) & (gdf['BEACH_CODE'] <= 8283)].copy()

# Dictionnaires fournis
cellules_hydrosedimentaires = {
    "Plage à Sable Blanc Sans Recif": [8212,8213,8214,8281],
    "Plage à Sable Blanc Avec Recif": [8192,8194,8195,8196,8197,8198,8199,8200,8201,8202,8203,8204,
                                   8205,8206,8207,8208,8209,8210,8211,8215,8216,8217,8221,8222,
                                   8223,8233,8234,8280],
    "Plage à Sable Noir Avec Recif": [8225,8226],
    "Plage à Sable Noir Sans Recif": [8224,8267,8271,8272,8277,8278,8279],
    "Plage Mixte Sans Recif": [8232,8268,8269,8270,8273,8275,8276,8283],
    "Plage Mixte Avec Recif": [8193,8218,8219,8220,8227],
    "Plage à Galets": [8228,8230,8231,8235,8237,8238,8239,8240,8241,8242,8243,8244,8245,8246,
                    8247,8248,8249,8250,8251,8253,8254,8255,8256,8257,8258,8259,8260,8262,8263,8265],
    "Embouchure et/ou Delta": [8223,8229,8236,8252,8261,8264,8266,8274,8282]
}

sites_beach_codes = {
    "Baie de Saint-Paul": [8272,8273,8274,8275,8276,8277,8278,8279],
    "Etang-Sale": [8223,8224,8225,8226,8227,8283],
    "Hermitage et La Saline": [8201,8202,8203,8204,8205,8006,8207,8208],
    "La Possession": [8267,8268],
    "Le Port": [8269,8270,8271],
    "Saint-Benoît": [8235,8236,8237,8238,8239,8240,8241,8242,8243,8244,8245,8246,8247,
                     8248,8249,8250,8251,8252,8253],
    "Saint-Denis": [8261,8262,8263,8264,8265,8266],
    "Saint Gille": [8192,8193,8194,8195,8196,8197,8198,8199,8200],
    "Saint Joseph": [8282],
    "Saint Leu": [8209,8210,8211,8212,8213,8214,8215,8216,8217,8218,8219,8220,8221,8222],
    "Saint Louis": [8228,8229,8230,8231,8232],
    "Saint Pierre": [8233,8234,8280,8281],
    "Sainte-Marie": [8258,8259,8260],
    "Sainte Suzanne": [8254,8255,8256,8257]
}

# Fonction pour assigner l’attribut "Cell_Hydro_Type"
def assign_cell_hydro_type(code):
    for typ, codes in cellules_hydrosedimentaires.items():
        if code in codes:
            return typ
    return "Non_Défini"

# Fonction pour assigner l’attribut "Site_Name"
def assign_site_name(code):
    for site, codes in sites_beach_codes.items():
        if code in codes:
            return site
    return "Non_Attribué"

# Appliquer les fonctions aux colonnes dans le GeoDataFrame
gdf['Cell_Hydro_Type'] = gdf['BEACH_CODE'].apply(assign_cell_hydro_type)
gdf['Site_Name'] = gdf['BEACH_CODE'].apply(assign_site_name)

# Chemin de sauvegarde
output_path = "/media/jonathan/Expansion/TDC/beaches_filtered.shp"

# Enregistrement
gdf.to_file(output_path)

print(f"Couche sauvegardée avec succès dans : {output_path}")
