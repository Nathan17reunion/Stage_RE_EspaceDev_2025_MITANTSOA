import os
import json
import re

def extraire_dates_acquisition(chemin):
    dates = []
    pattern = re.compile(r"\d{8}T\d{6}")

    # Parcours des sous-dossiers dans le dossier principal
    for sous_dossier in os.listdir(chemin):
        chemin_sous_dossier = os.path.join(chemin, sous_dossier)
        if os.path.isdir(chemin_sous_dossier):
            # Parcours des fichiers dans chaque sous-dossier
            for fichier in os.listdir(chemin_sous_dossier):
                match = pattern.search(fichier)
                if match:
                    dates.append(match.group())
    return dates

if __name__ == "__main__":
    chemin = "/media/jonathan/Expansion/TDC/Data_S2/"
    dates = extraire_dates_acquisition(chemin)

    if not dates:
        print("Aucune date d'acquisition trouvée.")
    else:
        print(f"{len(dates)} dates d'acquisition trouvées.")

    chemin_sortie = "/home/jonathan/Images/Fusion/"
    fichier_json_path = os.path.join(chemin_sortie, "Dates_acquisition_images_Sentinel-2.json")

    data_a_sauvegarder = {"Date": dates}

    os.makedirs(chemin_sortie, exist_ok=True)
    with open(fichier_json_path, "w") as fichier_json:
        json.dump(data_a_sauvegarder, fichier_json, indent=4)

    print(f"Fichier JSON créé ici : {fichier_json_path}")
