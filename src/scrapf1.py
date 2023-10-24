import re 
import pandas as pd 
import requests

from tools import Crawler

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
race_result = Crawler.extract_table(res , class_name='resultsarchive-table')
table = pd.DataFrame(race_result)

table = retire_bords(table)

table['Driver'] = table['Driver'].apply(transformer_observation) # il vaut mieux faire ça après concaténation 
