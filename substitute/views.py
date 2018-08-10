import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from .libs.api_interactions import Substitutes
from .forms import SignUpForm
from .libs.exceptions import NoProductError


def index(request):
    """ Home page of Pur Beurre """
    return render(request, "substitute/index.html")

def results(request):
    """ Page with results of a request """

    query = request.GET.get("query")
    try:
        substitutes = Substitutes(query=query)
        substitutes_request = substitutes.get_substitutes()
        # I use session to store the results of the user query
        request.session["substitutes"] = substitutes_request
        substitutes_list = []
        for product in substitutes_request:
            substitute = {
                "name": product.get("product_name_fr"),
                "nutriscore": product["nutrition_grade_fr"],
                "picture": product.get("image_url", ""),
                "id_product": product["code"]
            }
            substitutes_list.append(substitute)

        paginator = Paginator(substitutes_list, 12)
        page = request.GET.get("page")
        try:
            substitutes_results = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            substitutes_results = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            substitutes_results = paginator.page(paginator.num_pages)

        context = {
            "query": query,
            "substitutes": substitutes_results,
            "count": len(substitutes_list),
            'paginate': True
        }
    except NoProductError:
        context = {
            "query": query,
            "substitutes": [],
            "count": 0,
            'paginate': False
        }

    return render(request, "substitute/results.html", context)    
    
def details(request, product_id):
    """ Page with details of a selected substitute """

    try:
        # I use substitues stored in the session
        for substitute in request.session["substitutes"]:
            if substitute["code"] == product_id:
                context = {
                    "name": substitute.get("product_name_fr"),
                    "nutriscore": substitute["nutrition_grade_fr"],
                    "picture": substitute.get("image_url"),
                    "ingredients": substitute.get("ingredients_text_with_allergens_fr"),
                    "nutrition_picture": substitute.get("image_nutrition_url", ""),
                    "stores": substitute.get("stores")
                }
                break
    except KeyError:
        context = {"error": True}

    return render(request, "substitute/details.html", context)

def signup(request):
    """ Page to sign up """

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("index")
    else:
        form = SignUpForm()
    context = {"form": form}
    return render(request, "substitute/signup.html", context)