import requests

class OpenFoodFactsData:
    """
    Class to get data of products from the API OpenFoodFacts
    """

    def _get_data_from_api(self, query, nutriscore=""):
        """
        This function search a product in Open Food Facts from the query of the
        user
        """

        payload = {
            "search_terms": query,
            "action": "process",
            "nutrition_grades": nutriscore,
            "page_size": 100,
            "search_simple": 1,
            "json": 1,
        }
        search = requests.get(
                        "https://fr.openfoodfacts.org/cgi/search.pl",
                        params=payload
                        )
        data = search.json()
        return data

    def _get_category(self, query):
        """
        This function get the first french category of a product from the first
        result of a search
        """

        data = self._get_data_from_api(query)
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

    def get_substitutes(self, query):
        """
        This function get a list of substitues from the category of a sought
        product.
        """

        category = self._get_category(query)
        # I want only substitutes with a nutrition grade "a"
        substitutes = self._get_data_from_api(category, "a")
        return substitutes["products"]