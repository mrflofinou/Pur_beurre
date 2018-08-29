import re
import html

import requests
from django.db import transaction, IntegrityError
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .forms import SignUpForm
from .models import Product
from .libs.exceptions import NoProductError
from .libs.api_interactions import Substitutes, DataApiClient


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
                "nutriscore": product.get("nutrition_grade_fr", ""),
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
            # If page is out of range (e.g. 9999), deliver last page of results
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
    
    # I check if a product is already saved by a user.
    # The button to save will be disable if the relation alreday exists between
    # a user and a product.
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        existing_relation = user.products.filter(code=product_id).exists()
    else:
        existing_relation = False

    try:
        selected_product = [substitute
                            for substitute in request.session["substitutes"]
                            if substitute["code"] == product_id]
        if selected_product:
            substitute = selected_product[0]
            context = {
                "code": substitute["code"],
                "name": substitute.get("product_name_fr"),
                "nutriscore": substitute.get("nutrition_grade_fr", ""),
                "picture": substitute.get("image_url"),
                "ingredients": substitute.get("ingredients_text_with_allergens_fr", ""),
                "nutrition_picture": substitute.get("image_nutrition_url", ""),
                "stores": substitute.get("stores"),
                "already_saved": existing_relation
            }
        else:
            raise KeyError
    except KeyError:
        # When a session expired or didn't exists before,
        # the list of substitutes is lost or not exist.
        # exceptionally I make a request to the API to find a product when the
        # sesseion don't have substitue list or if the product isn't in it.
        api_request = DataApiClient(product_id = product_id)
        product = api_request.get_unique_product_from_api()
        context = {
            "code": product["code"],
            "name": product.get("product_name_fr"),
            "nutriscore": product.get("nutrition_grade_fr", ""),
            "picture": product.get("image_url"),
            "ingredients": product.get("ingredients_text_with_allergens_fr"),
            "nutrition_picture": product.get("image_nutrition_url", ""),
            "stores": product.get("stores"),
            "already_saved": existing_relation
        }

    return render(request, "substitute/details.html", context)

@transaction.atomic
def save_product(request):
    """ To save a product in a user account """
    if request.method == "POST":
        user = get_object_or_404(User, username=request.user)
        # I check if the product is already in the data base or not.
        if not Product.objects.filter(code=request.GET.get("code")).exists():
            try:
                with transaction.atomic():
                    product = Product(
                        code = request.POST.get("code", ""),
                        # To decode specials strings
                        name = html.unescape(request.POST.get("name", "")),
                        nutriscore = request.POST.get("nutriscore", ""),
                        url_picture = request.POST.get("picture", ""),
                    )
                    product.save()
                data = {
                    "new_product": True
                }
            except IntegrityError:
                data = {
                    "error": True
                }
        else:
            try:
                with transaction.atomic():
                    product = Product.objects.get(code=request.GET.get("code"))
                    data = {
                        "product_exists": True
                    }
            except IntegrityError:
                data = {
                    "error": True
                }                

        try:
            with transaction.atomic():
                product.users.add(user)
        except IntegrityError:
            data = {
                "error": True
            }                
    else:
        raise Http404("Cette page n'est pas excessible")

    return JsonResponse(data)

@transaction.atomic
def delete_product(request):
    """ To delete a product from an user account """

    if request.method == 'POST':
        user = get_object_or_404(User, username=request.user)
        try:
            with transaction.atomic():
                product = Product.objects.get(code=request.POST.get("code"))
                product.users.remove(user)
                data = {
                    "delete": True,
                }
        except:
            data = {
                "error": True
            }
    else:
        raise Http404("Cette page n'est pas excessible")

    return JsonResponse(data)

def my_products(request): # Faire une fonction helper ?
    """ Page to display the products saved by users """

    user = get_object_or_404(User, username=request.user)
    products = user.products.all().order_by("-id")
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
        products_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products_page = paginator.page(paginator.num_pages)

    context = {
        "query": "Mes produits",
        "substitutes": products_page,
        "count": len(products_list),
        'paginate': True,
        "my_products": True
    }

    return render(request, "substitute/results.html", context)

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

def my_account(request):
    user = get_object_or_404(User, username=request.user)
    context = {
        "title": "Mon compte",
        "username": user.username,
        "email": user.email
    }
    return render(request, "substitute/account.html", context)

def notices(request):
    return render(request, 'substitute/notices.html')





###############################################################################
#                                                                             #
############################## HELPER FUNCTION ################################
#                                                                             #
###############################################################################

# def data_display(request, products):
#     """
#     This function help to get data from data base to display products from an
#     user account
#     """
#     products_list = []
#     for product in products:
#         my_product = {
#             "name": product.name,
#             "nutriscore": product.nutriscore,
#             "picture": product.url_picture,
#             "id_product": product.code,
#         }
#         products_list.append(my_product)
#     paginator = Paginator(products_list, 12)
#     page = request.GET.get("page")
#     try:
#         products_page = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         products_page = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         products_page = paginator.page(paginator.num_pages)

#     return products_page, len(products_list)    
