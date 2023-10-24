"""
Scraping de données de benchmarks 

Script qui permet d'extraire les données de benchmarks de composants informatiques.
Les données de l'exctration sont disponibles dans le répertoire data. 

Fonctions:
    - extract_html: Récupère le contenu HTML.
    - extract_table: Extrait les données d'un tableau.

Auteur: [Val832]
Date de création: 17/10/2023
"""

import re
import concurrent.futures
import pandas as pd
import requests

from tools import Crawler, clean_df, Merge, tqdm_executor_map

# Liste des URL concernant les benchmarks des différents composants informatiques.
URLS = [
    {   "url": "https://www.memorybenchmark.net/ram_list.php",
        "url_headers": "https://www.memorybenchmark.net/ram.php?ram=Corsair+CM5S16GM4800A40N2+16GB&id=18343"
    },
    {
        "url": "https://www.harddrivebenchmark.net/hdd_list.php",
        "url_headers": "https://www.harddrivebenchmark.net/hdd.php?hdd=35TTFP6PCIE-256G&id=27777"
    },
    {
        "url": "https://www.videocardbenchmark.net/gpu_list.php",
        "url_headers": "https://www.videocardbenchmark.net/gpu.php?gpu=Radeon+R7+A10-7860K&id=3447"
    },
    {   "url": "https://www.cpubenchmark.net/cpu_list.php",
        "url_headers": "https://www.cpubenchmark.net/cpu.php?cpu=Intel+Core+i5-3437U+%40+1.90GHz&id=1828"
    },
    {
        "url": "https://www.memorybenchmark.net/ram_list-ddr4.php",
        "url_headers": "https://www.memorybenchmark.net/ram.php?ram=A-DATA+Technology+AD5U48008G-B+8GB&id=18348"
    }
]

# Expression régulière pour extraire le nom du composant à partir de l'URL.
REGEX_PATTERN = r"net\/(.*?)\.php"

for i in URLS:

    url = i['url']

    # Utilisation de l'expression régulière pour identifier le nom du composant depuis l'URL.
    match = re.search(REGEX_PATTERN, url)
    file_name = match.group(1) if match else 'unnamed'  # Nom du composant ou "unnamed" si non identifié.

    # Extraction du contenu HTML depuis l'URL.
    html_content = Crawler.extract_html(url)

    # Extraire des données du tableau HTML avec l'id 'cputable'.
    df1  = Crawler.extract_table(html_content, table_id='cputable')

    # Recherche du tableau avec l'id 'cputable' dans le contenu HTML.
    result = Crawler.find_element(html_content, tag='table', element_id='cputable')
    body = result.find('tbody')
    rows = body.find_all('tr')

    # Extraction de la base de l'URL pour construire les URLs complètes ultérieurement.
    base = re.search(r'(.*net/)', url).group(1)
    urls = []

    # Pour chaque ligne du tableau, on ajoute les liens à la liste 'urls'
    for row in rows:
        a = row.find('a')
        if a and a.get('href'):
            urls.append(base + a.get('href'))

    # Modification de certains liens en fonction de leur structure pour les rendre utilisables.
    for index, current_url in enumerate(urls):
        if  url == "https://www.videocardbenchmark.net/gpu_list.php": 
            urls[index] = current_url.replace("video_lookup", "gpu")
        else :
            urls[index] = current_url.replace("_lookup", "")

    # Création d'un df avec les liens et fusion horizontale avec le df princiapal
    df2 = pd.DataFrame({"lien" : urls})
    df = pd.concat([df1, df2], axis=1)

    # Formatage des NA et nettoyage
    df = clean_df.convert_str_na_to_nan(df,"NA")
    df = clean_df.drop_na(df)

    # Extraction du tableau de données manquantes depuis l'URL des headers.
    # À chaque échec de requete on pourra attribuer cette valeur prédéfinie
    na_table = Merge.missing_table(i["url_headers"])

    ##Utilisation d'un exécuteur avec multithreading pour extraire les données de tous les liens en parallèle.
    sessions = [requests.Session() for _ in range(len(df['lien']))]
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        all_data = tqdm_executor_map(executor, Merge.fetch_data, df['lien'], 
                                     [na_table]*len(df['lien']),sessions, total = len(df['lien']))

    # conversion des données extraites en data frame
    df2 = pd.DataFrame(all_data)

    # Réinitialisation des indices pour les deux DataFrames.
    df.reset_index(drop=True, inplace=True)
    df2.reset_index(drop=True, inplace=True)
   
    df = pd.concat([df, df2], axis=1)
    # Sauvegarde des données sous forme de fichier CSV associé au composant correspondant.
    df.to_csv(f"/Users/valentinnaud/Desktop/produit_digital/data/{file_name}.csv")
    