import os
import re
from collections import defaultdict

#root_path = r"D:\TDC\AWEINSH" 
#root_path = r"D:\TDC\AWEISH"
#root_path = r"D:\TDC\NDWI"
root_path = r"D:\TDC\MNDWI"

years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

folder_counts = defaultdict(int)  # Nombre de dossiers par année
file_counts = defaultdict(int)    # Nombre de fichiers "_lines.shp" par année

# Parcours de tous les dossiers
for folder_name in os.listdir(root_path):
    folder_path = os.path.join(root_path, folder_name)

    if os.path.isdir(folder_path):
        try:
            match = re.search(r'(\d{8})', folder_name)
            if match:
                year_str = match.group(1)[:4]
                year = int(year_str)

                if year in years:
                    folder_counts[year] += 1  # Compte le dossier

                    # Parcours des sous-dossiers et fichiers
                    for dirpath, _, filenames in os.walk(folder_path):
                        for filename in filenames:
                            if filename.endswith("_lines.shp"):
                                file_counts[year] += 1
            else:
                print(f"Aucune date trouvée dans : {folder_name}")
        except Exception as e:
            print(f"Erreur avec le dossier {folder_name}: {e}")

# Résultats
print("\nNombre total de dossiers d'images par année :")
for year in years:
    print(f"Année {year} : {folder_counts[year]} dossiers")

print("\nNombre total de fichiers '_lines.shp' par année :")
total_files = 0
for year in years:
    print(f"Année {year} : {file_counts[year]} fichiers")
    total_files += file_counts[year]

print(f"\nTotal général : {total_files} fichiers '_lines.shp'")
