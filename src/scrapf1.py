import re 
import pandas as pd 
import requests
import numpy as np
from tools import Crawler, tqdm_executor_map

import concurrent.futures

def retire_bords(df):
    """
    Retire la première et la dernière ligne d'un DataFrame.
    
    Paramètres:
    -----------
    df : pd.DataFrame
        Le DataFrame original.
        
    Retourne:
    --------
    pd.DataFrame
        Le DataFrame sans la première et la dernière ligne.
    """
    return df.iloc[1:-1]

def transformer_observation(obs):
    observations = re.findall(r'(\w+)\n(\w+)', obs)
    resultats = [f"{prenom} {nom}" for prenom, nom in observations]
    return ", ".join(resultats)

BASE  =  "https://www.formula1.com" 
URL = ("https://www.formula1.com/en/results.html/2023/races/1141/bahrain/race-result.html")



res = Crawler.extract_html(URL)
href = Crawler.find_elements(res, 'a', attrs_key= "data-name", attrs_value="year")


urls_year = []

for i in href :
    
    link = i.get('href')
    if link : 
        urls_year.append(BASE+link)

urls_gp = []
for year in urls_year : 

    req = Crawler.extract_html(year)
    races = Crawler.find_elements(res, 'a', attrs_key= "data-name", attrs_value="meetingKey")

    for race in races[1:] : 
        link = race.get('href')
        urls_gp.append(BASE+link)


def missing_table (valid_url) : 

    res = Crawler.extract_html(valid_url)

    valid_table = Crawler.extract_table(res , class_name='resultsarchive-table')
    valid_table.iloc[0, :] = np.nan

    missing_table = valid_table.head(1)
    retire_bords(missing_table)

    return missing_table



na_table = missing_table(URL)

    
def fetch_f1result (race, missing_table, session ) : 

    try : 

        res = Crawler.extract_html(race)
        table = Crawler.extract_table(res , class_name='resultsarchive-table')

        # Extraire l'année
        year_match = re.search(r"\d{4}", race)
        table['Season'] = int(year_match.group()) if year_match else None

        # Extraire le nom du Grand Prix (gp_name)
        gp_name_match = re.search(r"/([^/]+)/race-result.html$", race)
        table['Localisation'] = gp_name_match.group(1) if gp_name_match else None

        table = retire_bords(table)
        table['Driver'] = table['Driver'].apply(transformer_observation) 

    except : 

        table = missing_table
        year_match = re.search(r"\d{4}", race)
        table['Season'] = int(year_match.group()) if year_match else None
        gp_name_match = re.search(r"/([^/]+)/race-result.html$", race)
        table['Localisation'] = gp_name_match.group(1) if gp_name_match else None
    
    return table

sessions = [requests.Session() for _ in range(len(urls_gp))]
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    all_df = tqdm_executor_map(executor, fetch_f1result, urls_gp, 
                                     [na_table]*len(urls_gp),sessions, total = len(urls_gp))

df = pd.concat(all_df, ignore_index=True)

df.to_csv("/Users/valentinnaud/Desktop/scrap_projects/data/dataf1")
