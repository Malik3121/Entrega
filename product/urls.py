from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('ProductList/', ProductList.as_view()),
    path('ProductDetail/', ProductDetail.as_view()),
    path('MakerList/', MakerList.as_view()),
    path('MakerDetail/', MakerDetail.as_view()),
    path('CategoryList/', CategoryList.as_view()),
    path('CategoryDetail/', CategoryDetail.as_view())
]