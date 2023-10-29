import unittest
from bs4 import BeautifulSoup
from unittest.mock import patch
from requests.exceptions import RequestException
from src.tools import Crawler  

class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler()
    
    # ----- Tests pour extract_html -----
    def test_url_not_string(self):
        """L'URL devrait être une chaîne de caractères."""
        with self.assertRaises(ValueError):
            self.crawler.extract_html(123)

    @patch('requests.get')
    def test_extract_html_success(self, mock_get):
        """L'extraction réussie de HTML devrait retourner un objet BeautifulSoup."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html></html>"
        result = self.crawler.extract_html("https://www.example.com")
        self.assertIsInstance(result, BeautifulSoup)

    @patch('requests.get')
    def test_extract_html_failed_response(self, mock_get):
        """Une réponse HTTP échouée devrait retourner un dictionnaire avec un message d'erreur."""
        mock_get.return_value.status_code = 404
        result = self.crawler.extract_html("https://www.example.com")
        self.assertIsInstance(result, dict)
        self.assertIn("error", result)
        self.assertEqual(result["error"],  "error in get method: 404")
    
    # ----- Tests pour find -----
    def test_find_simple_tag(self):
        """La recherche d'une simple balise devrait retourner une liste de correspondances."""
        html_content = BeautifulSoup('<div class="test">Hello</div><div class="test1">World</div>', 'html.parser')
        result = self.crawler.find(html_content, "div")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Hello")
        self.assertEqual(result[1].text, "World")

    def test_find_tag_with_attributes(self):
        """La recherche d'une balise avec des attributs devrait retourner une liste de correspondances."""
        html_content = BeautifulSoup('<div class="test">Hello</div><div class="test1">World</div>', 'html.parser')
        result = self.crawler.find(html_content, "div", attrs_key="class", attrs_value="test1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "World")
    
    # ----- Tests pour extract_table -----
    def test_extract_table_with_class_name(self):
        """Une table devrait être extraite en fonction du nom de classe."""
        html_content = BeautifulSoup('<table class="sample_class"><tr><th>Header1</th></tr><tr><td>Data1</td></tr></table>', 'html.parser')
        df = self.crawler.extract_table(html_content, class_name="sample_class")
        self.assertTrue("Header1" in df.columns)
        self.assertEqual(df["Header1"].iloc[1], "Data1")

    def test_extract_table_with_id(self):
        """Une table devrait être extraite en fonction de l'ID."""
        html_content = BeautifulSoup('<table id="sample_id"><tr><th>Header1</th></tr><tr><td>Data1</td></tr></table>', 'html.parser')
        df = self.crawler.extract_table(html_content, table_id="sample_id")
        self.assertTrue("Header1" in df.columns)
        self.assertEqual(df["Header1"].iloc[1], "Data1")

    def test_missing_parameters(self):
        """Une exception devrait être levée si ni le nom de classe ni l'ID ne sont fournis."""
        html_content = BeautifulSoup('<table><tr><th>Header1</th></tr><tr><td>Data1</td></tr></table>', 'html.parser')
        with self.assertRaises(ValueError):
            self.crawler.extract_table(html_content)

    def test_table_not_found(self):
        """Une exception devrait être levée si la table n'est pas trouvée."""
        html_content = BeautifulSoup("<div>Contenu d'exemple</div>", 'html.parser')
        with self.assertRaises(ValueError):
            self.crawler.extract_table(html_content, class_name="classe_inexistante")

    def test_extract_data_into_dataframe(self):
        """Les données devraient être correctement extraites dans un DataFrame."""
        html_content = BeautifulSoup('<table class="sample_class"><tr><th>Header1</th><th>Header2</th></tr><tr><td>Data1</td><td>Data2</td></tr></table>', 'html.parser')
        df = self.crawler.extract_table(html_content, class_name="sample_class")
        self.assertEqual(len(df.columns), 2)
        self.assertTrue("Header1" in df.columns and "Header2" in df.columns)
        self.assertEqual(df["Header1"].iloc[1], "Data1")
        self.assertEqual(df["Header2"].iloc[1], "Data2")

if __name__ == "__main__":
    unittest.main()

