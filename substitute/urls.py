from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.results, name="results"),
    url(r'^(?P<product_id>[0-9]+)/$', views.details, name="details"),
    url(r'^ajax/save_product/$', views.save_product, name="save_product"),
    url(r'delete_product/(?P<product_id>[0-9]+)/$', views.delete_product, name="delete_product"),
    url(r'^my_products/$', views.my_products, name="my_products"),
    url(r'^my_account/$', views.my_account, name="my_account")
]
