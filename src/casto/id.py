import requests
from bs4 import BeautifulSoup
import json 
import re 
import pandas as pd 

# URL de départ 
url = "https://www.castorama.fr/jardin-et-terrasse/cat_id_3399.cat"

request = requests.get(url)
soup = BeautifulSoup(request.text, 'html.parser')

# Extraction du fichier json contenant les id 
script = soup.find('script', text=re.compile('window\.__data'))

json_text = re.search(r'^\s*window\.__data\s*=\s*({.*?})\s*;\s*$',
                      script.string, flags=re.DOTALL | re.MULTILINE).group(1)

# problème de syntaxe json (manque "")
json_text = json_text.replace('undefined', '"undefined"')

data = json.loads(json_text)
cat_id = data['category']['data']['attributes']['categories']

i = 3 
id_list = []
name_list = []
path_list = []

while i < len (cat_id) : 

    try : 
        id_list.append(cat_id[i]['categoryRef'])
        name_list.append(cat_id[i]['displayName'])
        path_list.append(cat_id[i]['htmlContentPath'])
        

        i = i+1
    
    except : 
        i=i+1
        pass

df = {'id' : id_list , 'name' : name_list, 'path' : path_list }

id_csv = pd.DataFrame(df)
id_csv.to_csv("/Users/valentinnaud/Desktop/projets/Casto/id.csv")



