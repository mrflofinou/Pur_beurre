import json
import re

import requests

from .exceptions import NoProductError

class DataApiClient:
    """
    Class to get data of products from the API OpenFoodFacts
    """

    def __init__(self, **kwargs):
        self.query = kwargs.get("query", "")
        self.category = kwargs.get("category", "")
        self.nutriscore = kwargs.get("nutriscore", "")
        self.product_id = kwargs.get("product_id", "")

    def get_products(self):
        """
        This method searchs a product in Open Food Facts from the query of the
        user
        """

        payload = {
            "search_terms2": self.query,
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": self.category,
            "tagtype_1": "nutrition_grades",
            "tag_contains_1": "contains",
            "tag_1": self.nutriscore,
            "sort_by": "popularity",
            "page_size": 50,
            "search_simple": 1,
            "json": 1
        }
        search = requests.get(
                        "https://fr.openfoodfacts.org/cgi/search.pl",
                        params=payload
                        )
        data = search.json()
        # return a list of dictionaries. Every product is a dictionary
        return data
    
    def get_product(self):
        """ This method get the details of a unique product """

        api_request = requests.get(
                            "https://world.openfoodfacts.org/api/v0/product/"
                            + f"{self.product_id}" + "json")
        product_data = api_request.json()
        product = product_data["product"]
        return product


class Substitutes:
    """ This class allows to find substitutes of food """

    NUTRITION_GRADES = ["a", "b", "c","d","e"]

    def __init__(self, query):
        self.query = query

    def _get_category(self):
        """
        This method get the category of a product
        """

        data = DataApiClient(query=self.query)
        data_from_api = data.get_products()["products"]
        try:
            if data_from_api:
                # I've made the choice to select the first product from
                # the results of the user's request, to find the category.
                product = data_from_api[0]
                # I choose the last categery of the list 'categories_hieararchy'
                category_hierarchy = product["categories_hierarchy"]
                category_extracted = category_hierarchy[-1]
                # I just want to keep the string after the caracters of the country
                # ex: "fr:pâte-a-tartiner"
                category_string = re.search(r":(.+)$", category_extracted)
                category = category_string.group(1)
                category = category.replace("-", " ")
            else:
                raise NoProductError
        except KeyError:
            raise NoProductError
        except IndexError:
            raise NoProductError
        return category

    def get_substitutes(self):
        """
        This method gets a list of substitues from the category of a searched
        product.
        """

        substitute_category = self._get_category()
        substitutes = []
        # index is used to choose a nutriscore in the next list and obtain
        # substitutes in function of the nutrition grade
        index = 0
        # The goal of this loop is to have substitutes in the same category of
        # the searched product. If the search with nutrition grade 'A' doesn't
        # have results, I search substitutes in same category but with higher
        # nutrition grade
        while len(substitutes) == 0:
            try:
                data = DataApiClient(
                                    category=substitute_category,
                                    nutriscore=self.NUTRITION_GRADES[index]
                                    )
                substitutes = data.get_products()["products"]
                index += 1
            except IndexError:
                substitutes = []
                break
        return substitutes