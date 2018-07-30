from django.shortcuts import render
from django.http import HttpResponse

from .libs.api_interactions import Substitutes


def index(request):
    """ Home page of Pur Beurre """

    return render(request, "substitute/index.html", locals())

def results(request):
    """ Page with results of a request """

    query = request.GET.get("query")
    # user_request = DataProviderClient(query=query)
    substitutes = Substitutes(query)
    substitutes_request = substitutes.get_substitutes()
    substitutes_list = []
    for product in substitutes_request:
        substitute = {
            "name": product.get("product_name_fr"),
            "nutriscore": product["nutrition_grade_fr"],
            "picture": product.get("image_url", ""),
            "id_product": product["code"]
        }
        substitutes_list.append(substitute)
    context = {
        "query": query,
        "substitutes": substitutes_list
    }
    return render(request, "substitute/results.html", context)
    
def details(request):
    """ Page with details of a selected substitute """

    
    return render(request, "substitute/details.html", locals())