from django.urls import path

from . import views

urlpatterns = [
    path('', views.bing_scraper),
]