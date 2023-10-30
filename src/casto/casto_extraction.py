# Importation des bibliothèques nécessaires
import json 
import re
import concurrent.futures
import pandas as pd 
import requests 

# Importation des fonctions et classes spécifiques au projet
from src.casto import Crawler, tqdm_executor_map
from tools_casto import fetch_casto_data

# URL de la page principale du site Castorama pour la catégorie "jardin et terrasse"
URL = "https://www.castorama.fr/jardin-et-terrasse/cat_id_3399.cat"

# Utilisation de la classe Crawler pour extraire le contenu HTML de l'URL spécifié
res = Crawler.extract_html(URL)

# Extraction d'un script particulier contenant des données sous forme de JSON
script = res.find('script', string=re.compile('window\.__data'))

# Utilisation d'une expression régulière pour extraire uniquement le JSON du script
json_text = re.search(r'^\s*window\.__data\s*=\s*({.*?})\s*;\s*$', script.string, 
                      flags=re.DOTALL | re.MULTILINE).group(1)

# Remplacement d'une syntaxe incorrecte dans le JSON
json_text = json_text.replace('undefined', '"undefined"')

# Conversion du texte JSON en objet Python
data = json.loads(json_text)

# Extraction des ID des catégories à partir de l'objet data
cat_id = data['category']['data']['attributes']['categories']

# Initialisation des listes pour stocker les ID, noms et chemins des catégories
id_list = []
name_list = []
path_list = []

# Les 3 premières observations ne contiennent pas d'ID valides, donc on commence à partir du quatrième élément
for id in cat_id[3:]:
    try:
        # Tentative d'extraction et d'ajout des informations à partir de chaque ID
        id_list.append(id['categoryRef'])
        name_list.append(id['displayName'])
        path_list.append(id['htmlContentPath'])
    except:
        # Si une erreur se produit lors de l'extraction, continuez sans ajouter l'ID à la liste
        pass

# Conversion des listes en un dictionnaire pour une meilleure organisation
dict_id = {'id': id_list, 'name': name_list, 'path': path_list}

# Conversion du dictionnaire en DataFrame pour faciliter les manipulations ultérieures
df_id = pd.DataFrame(dict_id)

# Création d'une session pour gérer les requêtes 
session = requests.Session()

# Utilisation du multithreading pour accélérer l'extraction des données de chaque ID
# L'extraction est réalisée en parallèle grâce à un pool de 5 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    query_list = tqdm_executor_map(executor, fetch_casto_data, df_id.to_dict(orient='records'),
                                [session]*len(df_id), total=len(df_id))

# Écriture des données extraites dans un fichier JSON
with open('data/castorama/data.json', 'w', encoding='utf-8') as f:
    json.dump(query_list, f, ensure_ascii=False, indent=4)
