from django.test import TestCase
import requests

# from .models import Category, Product


def _get_data_from_api(query, nutriscore=""):
    """
    This function search a product in Open Food Facts from the query of the user
    """

    payload = {
        "search_terms": query,
        "action": "process",
        "nutrition_grades": nutriscore,
        "search_simple": 1,
        "json": 1,
    }
    search = requests.get(
                    "https://fr.openfoodfacts.org/cgi/search.pl",
                    params=payload
                    )
    data = search.json()
    return data

def get_category(query):
    """
    This function get the first french category of a product from the first
    result of a search
    """

    data = _get_data_from_api(query)
    # I choose the first product in the list of results
    product = data["products"][0]
    # I choose the first category write in french (rule defines by myself)
    # The name of category looks like "fr:category-name"
    for category in product["categories_tags"]:
        if "fr" in category:
            french_category = category
            break
    # I just want to keep the string after "fr:"
    french_category = french_category[3:]
    french_category = french_category.replace("-", " ")
    return french_category

def get_substitutes(query):
    """
    This function get a list of substitues from a category of a sought product
    with the nutriscore A.
    """
    category = get_category(query)
    substitutes = _get_data_from_api(category, "a")
    return substitutes


class SearchAlgorithmeTestCase(TestCase):
    
    def test_api_returns_status_code_200(self):
        res = requests.get("https://fr.openfoodfacts.org/cgi/search.pl")
        self.assertEqual(res.status_code, 200)
    
    # Recherche de produit dans OFF
    # Tester le format de la réponse de l'API (contient les élémént dont on a besoin)
    def test_api_returns_list_of_products(self):
        data = _get_data_from_api("nutella")
        self.assertTrue(data["products"])

    # Tester qu'une catégorie est extraite de la réponse de l'API
    def test_get_category_from_product(self):
        category = get_category("nutella")
        self.assertEqual(category, "pates a tartiner")

    # Recherche de substituts
    def test_get_substitutes_returns_list_of_products(self):
        substitutes = get_substitutes("nutella")
        self.assertTrue(substitutes["products"])
        
 