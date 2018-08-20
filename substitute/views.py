import re

import requests
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .forms import SignUpForm
from .models import Product
from .libs.exceptions import NoProductError
from .libs.api_interactions import Substitutes


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
                    "code": substitute["code"],
                    "name": substitute.get("product_name_fr"),
                    "nutriscore": substitute.get("nutrition_grade_fr", ""),
                    "picture": substitute.get("image_url"),
                    "ingredients": substitute.get("ingredients_text_with_allergens_fr"),
                    "nutrition_picture": substitute.get("image_nutrition_url", ""),
                    "stores": substitute.get("stores")
                }
                break
    except KeyError:
        # When a session expired, the list of substitutes is lost.
        # exceptionally I make a request to the API to find a product when the
        # sesseion had expired after a logout of a user.
        # To have data of one product, the request to the API is different
        api_request = requests.get("https://world.openfoodfacts.org/api/v0/product/" + f"{product_id}" + "json")
        product_data = api_request.json()
        product = product_data["product"]
        context = {
            "code": substitute["code"],
            "name": product.get("product_name_fr"),
            "nutriscore": product.get("nutrition_grade_fr", ""),
            "picture": product.get("image_url"),
            "ingredients": product.get("ingredients_text_with_allergens_fr"),
            "nutrition_picture": product.get("image_nutrition_url", ""),
            "stores": product.get("stores")
        }

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

@transaction.atomic
def save_product(request):
    """ To save a product in a user account """

    try:
        with transaction.atomic():
            user = User.objects.get(username=request.user)
            product = Product(
                code = request.GET.get("code", ""),
                name = request.GET.get("name", ""),
                nutriscore = request.GET["nutriscore"],
                url_picture = request.GET.get("picture", ""),
                ingredients = request.GET.get("ingredients", ""),
                url_nutrition = request.GET.get("nutrition_picture", ""),
                stores = request.GET.get("stores", "")
            )
            product.save()
            product.users.add(user)
            data = {
                'new_product': Product.objects.filter(code=request.GET.get("code")).exists()
            }
    except IntegrityError:
        with transaction.atomic():
            product = Product.objects.get(code=request.GET.get("code"))
            product.users.add(user)
            data = {
                'product_exists': True
            }
    return JsonResponse(data)

def my_products(request):
    """ Page to display the products saved by users """

    user = User.objects.get(username=request.user)
    products = user.products.all()
    products_list = []
    for product in products:
        my_product = {
            "name": product.name,
            "nutriscore": product.nutriscore,
            "picture": product.url_picture,
            "id_product": product.code,
        }
        products_list.append(my_product)
    paginator = Paginator(products_list, 12)
    page = request.GET.get("page")
    try:
        products_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products_list = paginator.page(paginator.num_pages)

    context = {
        "query": "Mes produits",
        "substitutes": products_list,
        "count": len(products_list),
        'paginate': True,
         "my_products": True
    }

    return render(request, "substitute/results.html", context) 