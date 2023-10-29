"""
tools : Outils pour le traitement des données

Objectif :
-----------
Le module vise à fournir un ensemble d'outils pour faciliter le traitement des données,
depuis l'acquisition par le biais du web crawling jusqu'à la manipulation et la mise en forme
des dataframes.
"""

from bs4 import BeautifulSoup
import requests  
import pandas as pd 
from tqdm import tqdm
import re 
import numpy as np

class Crawler :

    """ [Class Docstring]
    Crawler: Classe d'extraction et d'analyse de contenu HTML.

    Cette classe est conçue pour extraire le contenu HTML d'une URL spécifiée et fournir 
    des méthodes pour explorer et extraire des informations spécifiques du contenu.

    Attributs:
    ----------
    Aucun

    Méthodes:
    ---------
    - extract_html(url: str) -> Union[BeautifulSoup, Dict[str, str]]:
        Effectue une requête HTTP GET à l'URL spécifiée et renvoie le contenu HTML ou un 
        message d'erreur.
    
    - find_elements(html_content: BeautifulSoup, tag: str, class_name: Optional[str], 
                    element_id: Optional[str]) -> Tuple[str, Union[List[BeautifulSoup], None]]:
        Recherche tous les éléments HTML correspondants dans le contenu fourni en fonction 
        du tag, du nom de classe ou de l'ID et renvoie un tuple contenant un message et la 
        liste des éléments correspondants.

    - find_element(html_content: BeautifulSoup, tag: str, class_name: Optional[str], 
                   element_id: Optional[str]) -> Union[BeautifulSoup, Dict[str, str]]:
        Recherche le premier élément HTML correspondant dans le contenu fourni et renvoie 
        l'élément ou un message d'erreur.

    - extract_table(html_content: BeautifulSoup, class_name: Optional[str], table_id: Optional[str]) -> pd.DataFrame:
        Extrait une table du contenu HTML fourni, la convertit en un DataFrame pandas et 
        renvoie le DataFrame.

    Exemple d'utilisation:
    ----------------------
    crawler = Crawler()
    html_content = crawler.extract_html("https://www.example.com")
    message, elements = crawler.find_elements(html_content, 'table', class_name='myTable')
    """

    @staticmethod
    def extract_html(url):

        """Paramètres:
        -----------
        url : str
            L'URL du site web dont vous souhaitez extraire le contenu HTML.

        Retourne:
        --------
        BeautifulSoup object or dict
            Si la requête est réussie (code HTTP 200), renvoie un objet BeautifulSoup contenant le contenu HTML de la page.
            Si la requête échoue, renvoie un dictionnaire contenant une clé "error" et un message d'erreur détaillé.

        Exceptions:
        ----------
        ValueError: Si l'URL fournie n'est pas de type 'string'.
        requests.RequestException: Si une exception liée à la requête se produit.
        """

        if not isinstance(url, str) : 
            raise ValueError("L'url saisie doit être de type 'string'")

        try:
            response = requests.get(url)

            # Si la requête est réussie (code 200), on renvoie le contenu HTML
            if response.status_code == 200:
                return BeautifulSoup(response.text, 'html.parser')

            # Sinon, on renvoie un dictionnaire d'erreur
            return {"error": f"error in get method: {response.status_code}"}
        
        # Gestion des exceptions liées aux requêtes
        except requests.RequestException as e:
            return {"error": f"An error occurred: {str(e)}"}
            
    @staticmethod
    def find(html_content, tag,  method = 0 , attrs_key = None, attrs_value = None):

        """ 
        Recherche tous les éléments HTML dans le contenu fourni en utilisant le tag et des attributs optionnels.

        Paramètres:
        -----------
        html_content : BeautifulSoup
            Objet BeautifulSoup contenant le contenu HTML à analyser.
        tag : str
            Tag HTML de l'élément à rechercher (par exemple, 'table', 'div', 'a', etc.).
        method : int, optional (default: 0)
            Méthode de recherche à utiliser: 0 pour "find_all" et 1 pour "find".
        attrs_key : str, optional
            Clé de l'attribut à utiliser pour la recherche (par exemple, 'class', 'id', etc.).
        attrs_value : str, optional
            Valeur de l'attribut à utiliser pour la recherche.

        Retourne:
        --------
        list ou BeautifulSoup object
            Liste des éléments trouvés ou un seul objet BeautifulSoup selon la méthode utilisée. 
            Si aucun élément n'est trouvé, renvoie une liste vide (pour "find_all") ou None (pour "find").

        Exceptions:
        ----------
        ValueError: Si l'objet html_content fourni n'est pas une instance de BeautifulSoup, 
        si le tag n'est pas une chaîne de caractères, si method n'est pas 0 ou 1, 
        ou si seulement l'une des valeurs attrs_key ou attrs_value est fournie.
        """

        # Vérification du type de l'objet html_content
        if not isinstance(html_content, BeautifulSoup): 
            raise ValueError("L'entrée doit être un objet BeautifulSoup.")
        
        if not isinstance(tag, str) : 
            raise ValueError("Le tag doit être de type 'string'.") 

        if method not in [0,1] : 
                raise ValueError("Veuillez saisir une méthode égale à 0 (find_all) ou 1 (find).")
        
        if attrs_key is not None : 
            if not isinstance(attrs_key, str) : 
                raise ValueError("attrs_key doit être de type 'string'.") 
        if attrs_value is not None : 
            if not isinstance(attrs_value, str) : 
                raise ValueError("attrs_value doit être de type 'string'.") 
        
        if (attrs_key is None  and attrs_value is not None) or (attrs_key is not None  and attrs_value is None) : 
            raise ValueError ("Les 2 arguements attrs_key et attrs_value doivent être renseignés.")

        if method == 0 : 
            if attrs_key is not None : 
                res = html_content.find_all(tag, attrs= {attrs_key : attrs_value})
            else : 
                res = html_content.find_all(tag)
        else  :
            if attrs_key is not None : 
                res = html_content.find(tag, attrs= {attrs_key : attrs_value})
            else : 
                res = html_content.find(tag)

        return res 
    
    @staticmethod  
    def extract_table(html_content, class_name=None, table_id=None):

        """ [Function Docstring]
        Extrait une table du contenu HTML fourni en utilisant soit 
        le nom de la classe `class_name` soit l'ID `table_id`.

        Paramètres:
        -----------
        html_content : BeautifulSoup
            Objet BeautifulSoup contenant le contenu HTML à analyser.
        class_name : str, optional
            Nom de la classe CSS de la table à extraire. 
            Utilisé pour la sélection de la table basée sur la classe.
        table_id : str, optional
            ID de la table à extraire. Utilisé pour la sélection de la table basée sur l'ID.

        Retourne:
        --------
        pd.DataFrame
            DataFrame contenant les données de la table extraites.

        Exceptions:
        ----------
        ValueError: Si l'objet `html_content` fourni n'est pas une instance de BeautifulSoup, 
        si la table n'est pas trouvée, ou si ni `class_name` ni `table_id` ne sont fournis.
        """

        if not isinstance(html_content, BeautifulSoup): 
            raise ValueError("L'entrée doit être un objet BeautifulSoup.")
        
        # Extrait la table en utilisant le nom de classe ou l'id
        if class_name is not None: 
            table = html_content.find('table', class_ = class_name)
        elif table_id is not None: 
            table = html_content.find('table', id=table_id)
        else:
            raise ValueError("L'un des deux paramètres class_name ou table_id doit être fourni.")
        
        # S'assure que la table est trouvée
        if table is None:
            raise ValueError("Table non trouvée.")
        
        # Extrait l'en-tête
        header = [th.text.strip() for th in table.find_all('th')]
            
        # Extrait les données des lignes
        rows_data = []
        for row in table.find_all('tr'):  # Exclut la ligne d'en-tête
            rows_data.append([td.text.strip() for td in row.find_all('td')])
                
        # Convertit en DataFrame
        df = pd.DataFrame(rows_data, columns=header)
        return df

class CleanDf : 

    @staticmethod
    def convert_str_na_to_nan(df, na_values):
        """
        Convertit les chaînes de caractères représentant des NA en NaN.

        Paramètres:
        - df (pd.DataFrame): Le DataFrame en entrée.
        - na_values (list of str): Liste des chaînes de caractères représentant des NA.

        Retourne:
        pd.DataFrame: DataFrame avec les chaînes représentant des NA converties en NaN.

        Exemple d'utilisation:
        convert_str_na_to_nan(df, na_values=["NA", "N/A", "null"])
        """
        return df.replace(na_values, pd.NA)

    @staticmethod
    def drop_na(df, col=None, cols=None):

        if not isinstance(df, pd.DataFrame):
            raise ValueError("L'entrée doit être un DataFrame Pandas.")

        # Vérifie si le paramètre `col` est utilisé.
        if col is not None:
            if col not in df.columns:
                raise ValueError(f"Colonne {col} non trouvée dans le DataFrame.")
            return df.dropna(subset=[col])

        # Vérifie si le paramètre `cols` est utilisé.
        elif cols is not None:
            # Vérifie que cols est une liste
            if not isinstance(cols, list):
                raise ValueError("L'argument `cols` doit être une liste de noms de colonnes.")

            # Vérifie que chaque élément de cols est une chaîne et qu'il existe dans le DataFrame
            for col_name in cols:
                if not isinstance(col_name, str):
                    raise ValueError("Tous les éléments de `cols` doivent être des chaînes représentant les noms de colonnes.")
                if col_name not in df.columns:
                    raise ValueError(f"Colonne {col_name} non trouvée dans le DataFrame.")
            
            return df.dropna(subset=cols)
        
        # Si ni `col` ni `cols` n'est spécifié, supprime les lignes avec NA dans toutes les colonnes.
        else:
            return df.dropna()
    
    @staticmethod
    def transformer_observation(obs):

        observations = re.findall(r'(\w+)\n(\w+)', obs)
        resultats = [f"{prenom} {nom}" for prenom, nom in observations]
        return ", ".join(resultats)
        
def tqdm_executor_map(executor, function, *args, **kwargs):
    """
    Une fonction pour exécuter une fonction de manière parallèle 
    tout en affichant une barre de progression avec tqdm.

    Arguments:
    - executor : Un exécuteur de type concurrent.futures 
    (ThreadPoolExecutor ou ProcessPoolExecutor).
    - function : La fonction à exécuter en parallèle.
    - *args : Les arguments à passer à la fonction.
    - **kwargs : Les arguments clé/valeur à passer à la fonction.

    Retourne :
    - Une liste des résultats renvoyés par la fonction.
    """

    # Définition des codes de couleur pour la barre de progression.
    DARK_GREEN = "\033[32m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    ENDC = "\033[0m"
    
    # Format personnalisé pour tqdm en utlisant les codes couleurs 
    bar_format = "{l_bar}" + DARK_GREEN + "█{bar:25}░" + ENDC + " " + RED + "{n_fmt}/{total_fmt}" + ENDC + " " + BLUE + "[{rate_fmt} eta {remaining}]" + ENDC

    # Utilise l'exécuteur pour exécuter la fonction en parallèle.
    gen = executor.map(function, *args)
    
    # Si un total est fourni dans kwargs, il est utilisé. Sinon, il est laissé à None.
    total = kwargs.get('total', None)
    
    # Enveloppe le générateur avec tqdm pour afficher la barre de progression.
    return list(tqdm(gen, 
                    desc="Processing data 🚀 ", 
                    bar_format=bar_format,
                    dynamic_ncols=True, 
                    mininterval=0.25,
                    total=total))
