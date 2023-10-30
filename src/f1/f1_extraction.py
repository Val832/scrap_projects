import pandas as pd 
import requests
import concurrent.futures

# Importation des modules nécessaires pour le web scraping
from src.f1 import Crawler, tqdm_executor_map
from tools_f1 import *

# URL de base du site 
BASE  =  "https://www.formula1.com" 

# URL servant de premier point d'entrée 
URL = ("https://www.formula1.com/en/results.html/2023/races/1141/bahrain/race-result.html")

# Extraire le contenu HTML de l'URL spécifié
res = Crawler.extract_html(URL)

# Chercher les liens correspondant aux différentes années de course disponibles sur la page
href = Crawler.find(res, 'a', attrs_key= "data-name", attrs_value="year")

urls_year = []

# Parcourir chaque élément trouvé pour extraire et construire les URLs complètes
for i in href:
    link = i.get('href')
    if link: 
        urls_year.append(BASE+link)

urls_gp = []

# Pour chaque année trouvée, chercher les liens des GP de cette année 
for year in urls_year:
    res = Crawler.extract_html(year)
    races = Crawler.find(res, 'a', attrs_key= "data-name", attrs_value="meetingKey")

    # Ajouter l'URL de chaque GP à la liste (en ignorant le premier qui n'est pas un GP)
    for race in races[1:]:
        link = race.get('href')
        urls_gp.append(BASE+link)

# Obtenir une structure/tableau de données manquantes pour être utilisée ultérieurement
na_table = f1_missing_table(URL)

# Création d'une cession permanante pour optimiser l'extraction 
session = requests.Session() 

# Utiliser un ThreadPool pour extraire en parallèle les données de chaque GP
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    all_df = tqdm_executor_map(executor, fetch_f1_data, urls_gp, 
                               [na_table]*len(urls_gp), [session]*len(urls_gp), total = len(urls_gp))

# Réinitialiser l'index pour chaque dataframe extrait
all_df = [df.reset_index(drop=True) for df in all_df]

df = pd.concat(all_df, ignore_index=True)
# Sauvegarder le dataframe résultant dans un fichier CSV
df.to_csv("data/f1/f1_data.csv")

