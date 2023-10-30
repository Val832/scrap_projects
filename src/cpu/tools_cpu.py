from src.cpu import Crawler

from src.cpu import Crawler

def missing_cpu_table(url): 
    """
    Extrait les en-têtes du tableau CPU et initialise un dictionnaire avec "NA" pour les données manquantes.

    Paramètres:
    - url (str): L'URL d'où le tableau doit être extrait.

    Retourne:
    - dict: Un dictionnaire avec les en-têtes comme clés et "NA" comme valeurs pour les données manquantes.
    """
    
    # Extraction du HTML de l'URL donné à l'aide de la classe Crawler
    res = Crawler.extract_html(url)
    
    # Recherche de l'élément de tableau souhaité dans le HTML extrait
    table = Crawler.find(res, tag='table', method=1,
                         attrs_key='id', attrs_value='test-suite-results')

    # Initialisation du dictionnaire pour les données manquantes
    missing_table = {}
    for row in table.findAll('tr'):
        header = row.find('th').text
        missing_table[header] = "NA"
        
    return missing_table

def fetch_cpu_data(url, missing_table, session):
    """
    Tente d'extraire les données du tableau CPU et retourne un dictionnaire rempli ou un dictionnaire avec des données manquantes.

    Paramètres:
    - url (str): L'URL d'où le tableau doit être extrait.
    - missing_table (dict): Un dictionnaire avec des en-têtes et des valeurs "NA" pour les données manquantes.
    - session: Session pour effectuer la requête.

    Retourne:
    - dict: Un dictionnaire avec les données extraites ou avec des données manquantes.
    """
    try:
        # Extraction du HTML de l'URL donné
        res = Crawler.extract_html(url)
        
        # Recherche du tableau souhaité
        table = Crawler.find(res, tag='table', method=1,  attrs_key='id', attrs_value='test-suite-results')
        
        # Extraction des données du tableau
        data = {}
        for row in table.findAll('tr'):
            header = row.find('th').text
            value = row.find('td').text
            data[header] = value
        return data 
    except:
        # Retourne le dictionnaire de données manquantes en cas d'erreur
        data = missing_table
        return data 
