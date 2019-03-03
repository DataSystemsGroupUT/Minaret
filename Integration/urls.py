"""Integration URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from forrmsApp.views import rapSearch, Results, About, Contact, poll_state, index2, showResults
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',rapSearch, name='rapSearch'),
    url(r'^index/$', rapSearch, name='rapSearch'),
    url(r'^Results/$', Results, name='Results'),
    url(r'^showResults/$', showResults, name='showResults'),
    url(r'^about/$', About, name='About'),
    url(r'^contact/$', Contact, name='Contact'),
    url(r'^poll_state/$', poll_state, name='poll_state'),
    url(r'^index2/$', index2, name='index2'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
