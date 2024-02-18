from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('CityViewSet/', CityViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('WeatherViewSet/', WeatherViewSet.as_view({'get': 'list', 'post': 'create'}))
]