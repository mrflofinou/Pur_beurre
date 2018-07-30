from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.results, name="results"),
    url(r'^details/$', views.details, name="details")
]
