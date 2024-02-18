from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('OrderViewSet/', OrderViewSet.as_view({'get': 'list', 'post': 'create'})),
]