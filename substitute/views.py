import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from .libs.api_interactions import Substitutes
from .forms import SignUpForm


def index(request):
    """ Home page of Pur Beurre """
    return render(request, "substitute/index.html")

def results(request):
    """ Page with results of a request """

    query = request.GET.get("query")
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
    context = {
        "query": query,
        "substitutes": substitutes_list
    }
    return render(request, "substitute/results.html", context)
    
def details(request, product_id):
    """ Page with details of a selected substitute """

    # I use substitues store in the session
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