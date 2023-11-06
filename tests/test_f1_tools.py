import unittest
from unittest.mock import patch, Mock
import pandas as pd
from src.f1.tools_f1 import fetch_f1_data, f1_missing_table  
import numpy as np
class TestF1Functions(unittest.TestCase):

    def setUp(self):
        # Initialisation des données qui seront utilisées dans les tests
        self.url_race_results = "https://example.com/2023/some_race/race-result.html"
        self.url_missing_table = "https://example.com/valid_url.html"
        # Création de données fictives pour simuler les résultats du scraping
        self.mock_race_results = pd.DataFrame({
            "a": ["None","a", "a"], 
            "Driver": ["None","Sergio\nPerez\nPER", "Max\nVerstappen\nVER"], 
            "Time": ["None","1:23.456", "1:24.567"],
            "b": ["None","a", "a"]
        })
        self.missing_table = pd.DataFrame({
            "Driver": ["NA"], 
            "Time": ["NA"],
            "Season": [2023],
            "Localisation":["some_race"]
        })
        # Message d'erreur pour simuler une table manquante
        self.session = Mock()

    def test_fetch_f1_data(self):
        # Utilisation de 'with' pour appliquer les patches
        with patch("src.tools.Crawler.extract_html") as mock_extract_html, \
             patch("src.tools.Crawler.extract_table") as mock_extract_table:
             
            # Configuration des objets mock avec les données initiales
            mock_extract_html.return_value = "<html>Contenu de test</html>"
            mock_extract_table.return_value = self.mock_race_results
            
            # Appel de la fonction à tester
            result_df = fetch_f1_data(self.url_race_results, self.missing_table, self.session)

            # Vérifications avec assertions
            self.assertTrue("Season" in result_df.columns)
            self.assertTrue("Localisation" in result_df.columns)
            self.assertEqual(result_df["Season"].iloc[0], 2023)
            self.assertEqual(result_df["Localisation"].iloc[0], "some_race")
            self.assertEqual(result_df["Driver"].iloc[0], "Sergio Perez")

    def test_f1_missing_table(self):
        # Utilisation de 'with' pour appliquer les patches
        with patch("src.tools.Crawler.extract_html") as mock_extract_html, \
             patch("src.tools.Crawler.extract_table") as mock_extract_table:
             
            # Configuration des objets mock pour simuler une erreur
            mock_extract_html.return_value = "<html>Contenu de test</html>"
            mock_extract_table.return_value = self.mock_race_results
            
            # Appel de la fonction à tester
            result_df = f1_missing_table(self.url_race_results)

            # Vérifications avec assertions
            self.assertTrue(result_df['Driver'].iloc[0], np.nan)

if __name__ == "__main__":
    unittest.main()
