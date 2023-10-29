import re 
import numpy as np 
from src.f1 import Crawler, CleanDf

def fetch_f1_data(race, missing_table, session): 
    """
    Récupère les données d'une course F1 depuis une URL spécifique.
    
    :param race: URL de la course F1 à scraper.
    :param missing_table: Tableau de secours à renvoyer si le scraping échoue.
    :param session: Session HTTP pour les requêtes.
    :return: DataFrame contenant les données de la course ou le tableau de secours en cas d'échec.
    """

    df_clean = CleanDf()  # Initialisation de l'outil de nettoyage des données

    try: 
        # Récupération du contenu HTML de la page de la course
        res = Crawler.extract_html(race)
        
        # Extraction du tableau des résultats de la course depuis le contenu HTML
        table = Crawler.extract_table(res, class_name='resultsarchive-table')

        # Extraction de l'année de la course depuis l'URL
        year_match = re.search(r"\d{4}", race)
        table['Season'] = int(year_match.group()) if year_match else None

        # Extraction du nom du Grand Prix depuis l'URL
        gp_name_match = re.search(r"/([^/]+)/race-result.html$", race)
        table['Localisation'] = gp_name_match.group(1) if gp_name_match else None

        # Élimination des lignes non pertinentes et nettoyage des données des pilotes
        table = table.iloc[1:-1]
        table['Driver'] = table['Driver'].apply(df_clean.transformer_observation) 

    except: 
        # En cas d'erreur lors du scraping, utiliser le tableau de secours
        table = missing_table
        year_match = re.search(r"\d{4}", race)
        table['Season'] = int(year_match.group()) if year_match else None
        gp_name_match = re.search(r"/([^/]+)/race-result.html$", race)
        table['Localisation'] = gp_name_match.group(1) if gp_name_match else None

    return table
    
def f1_missing_table(valid_url): 
    """
    Crée un tableau de secours en cas d'échec du scraping sur une URL valide.
    
    :param valid_url: URL valide à partir de laquelle le tableau de secours est généré.
    :return: DataFrame qui servira de tableau de secours en cas d'échec du scraping.
    """

    # Récupération du contenu HTML de la page valide
    res = Crawler.extract_html(valid_url)

    # Extraction du tableau depuis la page valide
    valid_table = Crawler.extract_table(res, class_name='resultsarchive-table')
    
    # Remplacement de la première ligne par NaN pour créer le tableau de secours
    valid_table.iloc[0, :] = np.nan
    missing_table = valid_table.head(1)
    missing_table = missing_table.iloc[1:-1]

    return missing_table
