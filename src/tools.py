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
    def extract_html(url: str):

        """ [Function Docstring]
        Extrait le contenu HTML d'une URL donnée.

        Paramètres:
        -----------
        url : str
            L'URL à partir de laquelle extraire le contenu HTML.

        Retourne:
        --------
        BeautifulSoup
            Une instance de BeautifulSoup contenant le contenu HTML si la requête est réussie.
        Dict[str, str]
            Un dictionnaire avec un message d'erreur si la requête échoue ou si un autre problème survient.

        Exemples:
        --------
        >>> extract_html("https://www.example.com")
        <html>...</html>

        >>> extract_html("https://www.invalid-url.com")
        {'error': 'An error occurred: ...'}
        """

        try:
            response = requests.get(url)

            # Si la requête est réussie (code 200), on renvoie le contenu HTML
            if response.status_code == 200:
                return BeautifulSoup(response.text, 'html.parser')

            # Sinon, on renvoie un dictionnaire d'erreur
            return print({"error": f"error in get method: {response.status_code}"})
        
        # Gestion des exceptions liées aux requêtes
        except requests.RequestException as e:
            return {"error": f"An error occurred: {str(e)}"}
            
    @staticmethod
    def find_elements(html_content, tag, class_name=None, element_id=None):

        """ [Function Docstring]
        Recherche tous les éléments HTML dans le contenu HTML fourni en utilisant le tag et le nom de la classe ou l'ID.

        Paramètres:
        -----------
        html_content : BeautifulSoup
            Objet BeautifulSoup contenant le contenu HTML à analyser.
        tag : str
            Tag HTML de l'élément à rechercher (par exemple, 'table', 'div', 'a', etc.).
        class_name : str, optional
            Nom de la classe CSS de l'élément à rechercher. Utilisé pour la sélection d'élément basée sur la classe.
        element_id : str, optional
            ID de l'élément à rechercher. Utilisé pour la sélection d'élément basée sur l'ID.

        Retourne:
        --------
        tuple (str, list of BeautifulSoup objects or None)
            Renvoie une paire (message, liste des éléments trouvés). Le message fournit le nombre de correspondances trouvées. Si aucun élément n'est trouvé, le message indique une absence de correspondance.

        Exemples:
        --------
        >>> from bs4 import BeautifulSoup
        >>> html = "<html><body><table class='myTable'><tr><td>Content</td></tr></table></body></html>"
        >>> soup = BeautifulSoup(html, 'html.parser')
        >>> message, elements = find_elements(soup, 'table', class_name='myTable')
        >>> print(message)
        1 correspondance(s) trouvée(s) avec le tag table et myTable

        Exceptions:
        ----------
        ValueError: Si l'objet html_content fourni n'est pas une instance de BeautifulSoup, ou si ni class_name ni element_id ne sont fournis.
        """

        # Vérification du type de l'objet html_content
        if not isinstance(html_content, BeautifulSoup): 
            raise ValueError("L'entrée doit être un objet BeautifulSoup.")
        
        # Recherche d'élément en utilisant le nom de la classe ou l'ID
        if class_name is not None: 
            res = html_content.find_all(tag, {'class': class_name})
        elif element_id is not None: 
            res = html_content.find_all(tag, id=element_id)
        else:
            raise ValueError("L'un des deux paramètres class_name ou element_id doit être fourni.")
        
        # Vérification du nombre d'éléments trouvés
        if res is None:
            return f"aucune correspondance avec le tag {tag} et {class_name or element_id}", None
        else:
            return f"{(len(res))} correspondance(s) trouvée(s) avec le tag {tag} et {class_name or element_id}", res

        
    @staticmethod
    def find_element(html_content, tag, class_name=None, element_id=None, attrs_key = None, attrs_value = None): 

        """ [Function Docstring]
        Recherche le premier élément HTML correspondant dans le contenu HTML fourni en utilisant le tag et le nom de la classe ou l'ID.

        Paramètres:
        -----------
        html_content : BeautifulSoup
            Objet BeautifulSoup contenant le contenu HTML à analyser.
        tag : str
            Tag HTML de l'élément à rechercher (par exemple, 'table', 'div', 'a', etc.).
        class_name : str, optional
            Nom de la classe CSS de l'élément à rechercher. Utilisé pour la sélection d'élément basée sur la classe.
        element_id : str, optional
            ID de l'élément à rechercher. Utilisé pour la sélection d'élément basée sur l'ID.

        Retourne:
        --------
        BeautifulSoup object or dict
            Retourne le premier élément BeautifulSoup trouvé. Si aucun élément n'est trouvé, retourne un dictionnaire avec un message d'erreur.

        Exemples:
        --------
        >>> from bs4 import BeautifulSoup
        >>> html = "<html><body><div class='myDiv'>Content</div></body></html>"
        >>> soup = BeautifulSoup(html, 'html.parser')
        >>> element = find_element(soup, 'div', class_name='myDiv')
        >>> print(element)
        <div class="myDiv">Content</div>

        Exceptions:
        ----------
        ValueError: Si l'objet html_content fourni n'est pas une instance de BeautifulSoup, ou si ni class_name ni element_id ne sont fournis.
        """
        
        # Vérification du type de l'objet html_content
        if not isinstance(html_content, BeautifulSoup): 
            raise ValueError("L'entrée doit être un objet BeautifulSoup.")
        
        # Recherche d'élément en utilisant le nom de la classe ou l'ID
        # Si class_name est fourni, recherche par classe
        if class_name is not None: 
            res = html_content.find(tag, {'class': class_name})
        # Si element_id est fourni, recherche par ID
        elif element_id is not None: 
            res = html_content.find(tag, id=element_id)
        # Si aucun n'est fourni, lève une exception
        elif attrs_key and attrs_value is not None : 
            res = html_content.find(tag, attrs= {attrs_key : attrs_value})
        else:
            raise ValueError("L'un des deux paramètres class_name ou element_id doit être fourni.")
        
        # Si aucun élément n'est trouvé, retourne un dictionnaire contenant un message d'erreur
        if res is None :
            return {f"aucune correspondance avec le tag {tag} et {class_name or element_id}"}  
        # Si un élément est trouvé, imprime un message et retourne l'élément trouvé
        else:
            return res

    @staticmethod  
    def extract_table(html_content, class_name=None, table_id=None):

        """ [Function Docstring]
        Extrait une table du contenu HTML fourni en utilisant soit le nom de la classe `class_name` soit l'ID `table_id`.

        Paramètres:
        -----------
        html_content : BeautifulSoup
            Objet BeautifulSoup contenant le contenu HTML à analyser.
        class_name : str, optional
            Nom de la classe CSS de la table à extraire. Utilisé pour la sélection de la table basée sur la classe.
        table_id : str, optional
            ID de la table à extraire. Utilisé pour la sélection de la table basée sur l'ID.

        Retourne:
        --------
        pd.DataFrame
            DataFrame contenant les données de la table extraites.

        Exceptions:
        ----------
        ValueError: Si l'objet `html_content` fourni n'est pas une instance de BeautifulSoup, si la table n'est pas trouvée, ou si ni `class_name` ni `table_id` ne sont fournis.

        Exemples:
        --------
        >>> from bs4 import BeautifulSoup
        >>> html = "<html><body><table class='myTable'><tr><th>Header</th></tr><tr><td>Data</td></tr></table></body></html>"
        >>> soup = BeautifulSoup(html, 'html.parser')
        >>> df = extract_table(soup, class_name='myTable')
        >>> print(df)
        Header
        0   Data
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
        for row in table.find_all('tr')[1:]:  # Exclut la ligne d'en-tête
            rows_data.append([td.text.strip() for td in row.find_all('td')])
                
        # Convertit en DataFrame
        df = pd.DataFrame(rows_data, columns=header)
        return df

class clean_df : 

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
        
class Merge :

    def missing_table (url): 

        res = Crawler.extract_html(url)
        table = Crawler.find_element(res, tag='table', element_id='test-suite-results')

        missing_table = {}
        for row in table.findAll('tr'):
            header = row.find('th').text
            missing_table[header] = "NA"
        
        return missing_table
    
    def fetch_data(url, missing_table, session):
        try :
            res = Crawler.extract_html(url)
            table = Crawler.find_element(res, tag='table', element_id='test-suite-results')
            data = {}
            for row in table.findAll('tr'):
                header = row.find('th').text
                value = row.find('td').text
                data[header] = value
            return data 
        except: 
            data = missing_table
            return data 
        
def tqdm_executor_map(executor, function, *args, **kwargs):
    """
    Une fonction pour exécuter une fonction de manière parallèle tout en affichant une barre de progression avec tqdm.

    Arguments:
    - executor : Un exécuteur de type concurrent.futures (ThreadPoolExecutor ou ProcessPoolExecutor).
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
