import requests

class DataProviderClient:
    """
    Class to get data of products from the API OpenFoodFacts
    """

    # modifier les paramètres de la fonction (**kwargs)
    def _get_data_from_api(self, query="", category="", nutriscore=""):
        """
        This function search a product in Open Food Facts from the query of the
        user
        """

        payload = {
            "search_terms2": query,
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "tagtype_1": "nutrition_grades",
            "tag_contains_1": "contains",
            "tag_1": nutriscore,
            "page_size": 100,
            "search_simple": 1,
            "json": 1
        }
        search = requests.get(
                        "https://fr.openfoodfacts.org/cgi/search.pl",
                        params=payload
                        )
        data = search.json()
        return data

    def _get_category(self, query):
        """
        This method get the category of a product
        """

        data = self._get_data_from_api(query=query)
        # I choose the first product in the list of results
        product = data["products"][0]
        # I choose the last categery of the list 'categories_hieararchy'
        category = product["categories_hierarchy"]
        category = category[-1]
        # I just want to keep the string after the caracters of the country
        # ex: "fr:"
        category = category[3:].replace("-", " ")
        return category

    def get_substitutes(self, query):
        """
        This method get a list of substitues from the category of a sought
        product.
        """

        substitute_category = self._get_category(query)
        # I want only substitutes with a nutrition grade "a"
        substitutes = self._get_data_from_api(category=substitute_category, nutriscore="a")
        return substitutes["products"]