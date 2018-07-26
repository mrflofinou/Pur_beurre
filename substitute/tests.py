from django.test import TestCase
import requests

from .libs.api_interactions import DataApiClient, Substitutes


class SearchAlgorithmeTestCase(TestCase):

    def setUp(self):
        self.user_request = DataApiClient()
        self.substitutes = Substitutes("")
    
    def test_api_returns_status_code_200(self):
        res = requests.get("https://fr.openfoodfacts.org/cgi/search.pl")
        self.assertEqual(res.status_code, 200)
    
    # Recherche de produit dans OFF
    # Tester le format de la réponse de l'API (contient les élémént dont on a besoin)
    def test_api_returns_list_of_products(self):
        self.user_request.query = "nutella"
        data = self.user_request.get_data_from_api()
        self.assertTrue(len(data) > 0)

    # Tester qu'une catégorie est extraite de la réponse de l'API
    def test_get_category_from_product(self):
        self.substitutes.query = "nutella"
        category = self.substitutes._get_category()
        self.assertEqual(category, "Pâtes à tartiner")

    # Recherche de substituts
    def test_get_substitutes_returns_products_with_nutella(self):
        self.substitutes.query = "nutella"
        substitutes_list = self.substitutes.get_substitutes()
        self.assertEqual(len(substitutes_list), 5)
    
    def test_get_substitutes_not_returns_products_with_petit_ecolier(self):
        self.substitutes.query = "petit écolier"
        substitutes_list = self.substitutes.get_substitutes()
        self.assertEqual(len(substitutes_list), 7)
    
    def test_app_return_substitutes(self):
        products = ["nutella", "coca-cola", "belvita", "eau de source", "granola", "jambon", "prince", "kiri", "eau minérale gazeuse", "ketchup", "muesli", "moutarde de dijon", "ice tea", "chocolat au lait", "pain de mie", "ricoré", "pringles", "biscuits sésame", "Oreo", "tagada", "thon entier au naturel", "lait", "knaki", "petit beurre", "nesquik", "jus d'orange", "lardons", "coco pops", "cracottes", "oasis", "activia", "yaourt aux fruits", "chavroux", "fromage", "perrier", "crunch", "tomacouli", "ebly", "m&ms", "chocapic", "st hubert", "margarine", "lasagne bolognaise", "danette", "ravioli boeuf", "coquillettes", "mousline", "steak haché", "pain au lait", "confiture framboise"]
        count = 0
        no_results_products = []
        for product in products:
            self.substitutes.query = product
            substitutes_list = self.substitutes.get_substitutes()
            if len(substitutes_list) > 0: 
                count += 1
            else:
                no_results_products.append(product)
        print(len(products), count, len(no_results_products), no_results_products)
        self.assertTrue(count > 42)