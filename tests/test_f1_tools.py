import unittest
from unittest.mock import patch, Mock
import pandas as pd
from src.f1.tools_f1 import fetch_f1_data, f1_missing_table  

class TestF1Functions(unittest.TestCase):

    @patch("src.tools.Crawler.extract_html")
    @patch("src.tools.Crawler.extract_table")
    def test_fetch_f1_data(self, mock_extract_table, mock_extract_html):
        # Configuration des mocks
        mock_extract_html.return_value = "<html>Test content</html>"
        mock_extract_table.return_value = pd.DataFrame({"Driver": ["A. Driver", "B. Driver"], "Time": ["1:23.456", "1:24.567"]})
        
        # Appel de la fonction
        result_df = fetch_f1_data("https://example.com/2023/some_race/race-result.html", None, None)
        
        # Assertions
        self.assertTrue("Season" in result_df.columns)
        self.assertTrue("Localisation" in result_df.columns)
        self.assertEqual(result_df["Season"].iloc[0], 2023)
        self.assertEqual(result_df["Localisation"].iloc[0], "some_race")

    @patch("src.tools.Crawler.extract_html")
    @patch("src.tools.Crawler.extract_table")
    def test_f1_missing_table(self, mock_extract_table, mock_extract_html):
        # Configuration des mocks
        mock_extract_html.return_value = "<html>Test content</html>"
        mock_extract_table.return_value = pd.DataFrame({"Driver": ["A. Driver", "B. Driver"], "Time": ["1:23.456", "1:24.567"]})
        
        # Appel de la fonction
        result_df = f1_missing_table("https://example.com/valid_url.html")
        
        # Assertions
        self.assertEqual(len(result_df), 1)
        self.assertTrue(pd.isna(result_df["Driver"].iloc[0]))

if __name__ == "__main__":
    unittest.main()
