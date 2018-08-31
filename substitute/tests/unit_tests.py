from django.test import TestCase
from unittest.mock import patch

import requests

from ..libs.api_interactions import DataApiClient, Substitutes


class SearchAlgorithmeTestCase(TestCase):

    def setUp(self):
        self.user_request = DataApiClient()
        self.substitutes = Substitutes("")
    
    def test_api_returns_status_code_200(self):
        res = requests.get("https://fr.openfoodfacts.org/cgi/search.pl")
        self.assertEqual(res.status_code, 200)
    
    def test_api_returns_list_of_products(self):
        self.user_request.query = "nutella"
        data = self.user_request.get_data_from_api()["products"]
        self.assertTrue(len(data) > 0)
    
    def test_api_request_unique_product_returns_dictionnary(self):
        self.user_request.product_id = "3175681105393"
        data = self.user_request.get_unique_product_from_api()
        self.assertEqual(f"{type(data)}", "<class 'dict'>")

    @patch("substitute.libs.api_interactions.DataApiClient.get_data_from_api")
    def test_get_category_from_product(self, mock_get_data_from_api):
        mock_get_data_from_api.return_value = {
            "products": [
                {
                    "categories_hierarchy": [
                        "fr:trucs sucrés",
                        "fr:trucs qui fondent",
                        "fr:trucs aux chocolats",
                        "fr:Pâtes à tartiner"
                    ]
                }
            ]
        }
        self.substitutes.query = "nutella"
        category = self.substitutes._get_category()
        self.assertEqual(category, "Pâtes à tartiner")

    @patch("substitute.libs.api_interactions.DataApiClient.get_data_from_api")
    @patch("substitute.libs.api_interactions.Substitutes._get_category")
    def test_get_substitutes_returns_substitutes_of_nutella(self, mock_get_category, mock_get_data_from_api):
        mock_get_category.return_value = "Pâte à tartiner"
        
        mock_get_data_from_api.return_value = {
            "products": [
                {
                    "name": "test1"
                },
                {
                    "name": "test2"
                },
                {
                    "name": "test3"
                },
                {
                    "name": "test4"
                },
                {
                    "name": "test1"
                }
            ]
        }
        
        self.substitutes.query = "nutella"
        substitutes_list = self.substitutes.get_substitutes()
        self.assertEqual(len(substitutes_list), 5)

    @patch("substitute.libs.api_interactions.DataApiClient.get_data_from_api")
    @patch("substitute.libs.api_interactions.Substitutes._get_category")
    def test_get_substitutes_returns_empty_list_if_no_substitutes(self, mock_get_category, mock_get_data_from_api):
        mock_get_category.return_value = "Pâte à tartiner"
        
        mock_get_data_from_api.return_value = {
            "products": []
        }
        
        self.substitutes.query = "nutella"
        substitutes_list = self.substitutes.get_substitutes()
        self.assertEqual(len(substitutes_list), 0)
    
    def test_app_return_substitutes(self):
        products = [
            "nutella", "coca-cola", "belvita", "eau de source", "granola",
            "jambon", "prince", "kiri", "eau minérale gazeuse", "ketchup",
            "muesli", "moutarde de dijon", "ice tea", "chocolat au lait",
            "pain de mie", "ricoré", "pringles", "biscuits sésame", "Oreo",
            "tagada", "thon entier au naturel", "lait", "knacki",
            "petit beurre", "nesquik", "jus d'orange", "lardons",
            "coco pops", "cracottes", "oasis", "activia",
            "yaourt aux fruits", "chavroux", "fromage", "perrier", "crunch",
            "tomacouli", "ebly", "m&ms", "chocapic", "st hubert",
            "margarine", "lasagne bolognaise", "danette", "ravioli boeuf",
            "coquillettes", "mousline", "steak haché", "pain au lait",
            "confiture framboise"
            ]
        count = 0
        no_results_products = []
        for product in products:
            substitutes = Substitutes(product)
            substitutes_list = substitutes.get_substitutes()
            if len(substitutes_list) > 0: 
                count += 1
            else:
                no_results_products.append(product)
            success_percentage = (count*100/50)
        print(len(no_results_products), no_results_products)
        self.assertTrue(success_percentage >= 95)