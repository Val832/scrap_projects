import re
import concurrent.futures
import pandas as pd
import requests


from src.cpu import Crawler, CleanDf, tqdm_executor_map
from tools_cpu import fetch_cpu_data, missing_cpu_table

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
    result = Crawler.find(html_content, tag='table',method=1, attrs_key='id',attrs_value='cputable')
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
    df = CleanDf.convert_str_na_to_nan(df,"NA")
    df = CleanDf.drop_na(df)

    # Extraction du tableau de données manquantes depuis l'URL des headers.
    # À chaque échec de requete on pourra attribuer cette valeur prédéfinie
    na_table = missing_cpu_table(i["url_headers"])

    #création d'une session permanante pour rendre l'extration plus rapide. 
    session = requests.Session() 

    # Utilisation d'un exécuteur avec multithreading pour 
    # Extraire les données de tous les liens en parallèle.
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        all_data = tqdm_executor_map(executor, fetch_cpu_data, df['lien'], 
                                     [na_table]*len(df['lien']),[session]*len(df['lien']), total = len(df['lien']))

    # Conversion des données extraites en data frame
    df2 = pd.DataFrame(all_data)

    # Réinitialisation des indices pour les deux DataFrames.
    df.reset_index(drop=True, inplace=True)
    df2.reset_index(drop=True, inplace=True)
   
    df = pd.concat([df, df2], axis=1)
    # Sauvegarde des données sous forme de fichier CSV associé au composant correspondant.
    df.to_csv(f"data/cpu/{file_name}.csv")
    