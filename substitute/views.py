from django.shortcuts import render
from django.http import HttpResponse

from .libs.api_interactions import DataProviderClient


def index(request):
    """ Home page of Pur Beurre """

    return render(request, "substitute/index.html", locals())

def results(request):
    """ Page with results of a request """

    query = request.GET.get("query")
    user_request = DataProviderClient()
    substitutes_request = user_request.get_substitutes(query)
    substitutes = []
    for product in substitutes_request:
        substitute = {
            "name": product.get("product_name_fr"),
            "nutriscore": product["nutrition_grade_fr"],
            "picture": product.get("image_url", ""),
            "id_product": product["code"]
        }
        substitutes.append(substitute)
    context = {
        "query": query,
        "substitutes": substitutes
    }
    return render(request, "substitute/results.html", context)
    