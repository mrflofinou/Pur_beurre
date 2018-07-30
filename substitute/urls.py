from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.results, name="results"),
    url(r'^(?P<product_id>[0-9]+)/$', views.details, name="details")
]
