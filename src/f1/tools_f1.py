import re 
import numpy as np 
from src.f1 import Crawler, CleanDf


def fetch_f1_data (race, missing_table, session ) : 

    df_clean = CleanDf()
    try : 
        res = Crawler.extract_html(race)
        table = Crawler.extract_table(res , class_name='resultsarchive-table')

        # Extraire l'année
        year_match = re.search(r"\d{4}", race)
        table['Season'] = int(year_match.group()) if year_match else None

        # Extraire le nom du Grand Prix (gp_name)
        gp_name_match = re.search(r"/([^/]+)/race-result.html$", race)
        table['Localisation'] = gp_name_match.group(1) if gp_name_match else None

        table = table.iloc[1:-1]
        table['Driver'] = table['Driver'].apply(df_clean.transformer_observation) 

    except : 
        table = missing_table
        year_match = re.search(r"\d{4}", race)
        table['Season'] = int(year_match.group()) if year_match else None
        gp_name_match = re.search(r"/([^/]+)/race-result.html$", race)
        table['Localisation'] = gp_name_match.group(1) if gp_name_match else None

    return table
    
def f1_missing_table(valid_url) : 

    res = Crawler.extract_html(valid_url)

    valid_table = Crawler.extract_table(res , class_name='resultsarchive-table')
    valid_table.iloc[0, :] = np.nan

    missing_table = valid_table.head(1)
    missing_table = missing_table.iloc[1:-1]

    return missing_table
            