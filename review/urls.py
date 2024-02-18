from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('ReviewViewSet/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}))
]
