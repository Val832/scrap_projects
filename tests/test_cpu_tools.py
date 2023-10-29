import unittest
from unittest.mock import Mock, patch
from src.cpu.tools_cpu import missing_cpu_table, fetch_cpu_data

class TestCpuFunctions(unittest.TestCase):

    def setUp(self):
        # Données fictives pour les tests
        self.url = "https://example.com/cpu"
        self.missing_table = {
            "Header1": "NA",
            "Header2": "NA",
        }
        self.session = Mock()

    def test_missing_cpu_table(self):
        # Mock du retour de la fonction Crawler.extract_html et Crawler.find
        with patch('src.tools.Crawler.extract_html') as mock_extract, \
             patch('src.tools.Crawler.find') as mock_find:

            
            mock_extract.return_value = "<html></html>"  # HTML fictif
            mock_find.return_value = Mock()  # Objet Mock pour simuler le tableau
            mock_row1 = Mock()
            mock_row1.find.return_value.text = "Header1"
            mock_row2 = Mock()
            mock_row2.find.return_value.text = "Header2"
            mock_find.return_value.findAll.return_value = [mock_row1, mock_row2]

            result = missing_cpu_table(self.url)
            self.assertEqual(result, self.missing_table)

    def test_fetch_cpu_data(self):
        # Mock du retour de la fonction Crawler.extract_html et Crawler.find
        with patch('src.tools.Crawler.extract_html') as mock_extract, \
             patch('src.tools.Crawler.find') as mock_find:

            mock_extract.return_value = "<html></html>"  # HTML fictif
            mock_find.return_value = Mock()  # Objet Mock pour simuler le tableau
            mock_find.return_value.findAll.return_value = [
                Mock(find=lambda tag: Mock(text="Header1" if tag == "th" else "Value1")),
                Mock(find=lambda tag: Mock(text="Header2" if tag == "th" else "Value2")),
            ]

            expected_data = {
                "Header1": "Value1",
                "Header2": "Value2",
            }

            result = fetch_cpu_data(self.url, self.missing_table, self.session)
            self.assertEqual(result, expected_data)

    def test_fetch_cpu_data_error(self):
        # Test pour le scénario où une erreur se produit (par exemple, si le tableau est introuvable)
        with patch('src.tools.Crawler.extract_html') as mock_extract, \
             patch('src.tools.Crawler.find', side_effect=Exception("Erreur")):

            mock_extract.return_value = "<html></html>"  # HTML fictif

            result = fetch_cpu_data(self.url, self.missing_table, self.session)
            self.assertEqual(result, self.missing_table)

if __name__ == "__main__":
    unittest.main()

