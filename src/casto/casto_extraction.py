import json 
import re
import concurrent.futures
import pandas as pd 
import requests 


from tools import Crawler, tqdm_executor_map, FetchData

# URL de départ 
URL = "https://www.castorama.fr/jardin-et-terrasse/cat_id_3399.cat"
res = Crawler.extract_html(URL)

# Extraction du fichier json contenant les id 
script = res.find('script', string=re.compile('window\.__data'))
json_text = re.search(r'^\s*window\.__data\s*=\s*({.*?})\s*;\s*$',
                      script.string, flags=re.DOTALL | re.MULTILINE).group(1)

# problème de syntaxe json (manque "")
json_text = json_text.replace('undefined', '"undefined"')

data = json.loads(json_text)
cat_id = data['category']['data']['attributes']['categories']

id_list = []
name_list = []
path_list = []

# Les 3 premières observations ne sont pas des id
for id in cat_id[3:]  : 

    try : 
        id_list.append(id['categoryRef'])
        name_list.append(id['displayName'])
        path_list.append(id['htmlContentPath'])    
    except : 
        pass

dict_id = {'id' : id_list , 'name' : name_list, 'path' : path_list }
df_id = pd.DataFrame(dict_id)
df_id = df_id[:50]
sessions = [requests.Session() for _ in range(len(df_id))]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    query_list = tqdm_executor_map(executor, FetchData.fetch_casto_data, df_id.to_dict(orient='records'), 
                                sessions, total = len(df_id))
            
print(len(query_list))

with open('/Users/valentinnaud/Desktop/scrap_projects/data/castorama/data.json', 'w', encoding='utf-8') as f:
    json.dump(query_list, f, ensure_ascii=False, indent=4)
