"""purbeurre_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from substitute import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^substitute/', include('substitute.urls', namespace="substitute")),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name="substitute/login.html"), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page="index"), name="logout"),
    url(r'^my_account/$', views.my_account, name="my_account"),
    url(r'^notices/$', views.notices, name="notices"),
    url(r'^control/$', admin.site.urls)
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns