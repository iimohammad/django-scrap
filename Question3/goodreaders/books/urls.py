from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # URL for the index view
    path('search/', views.search, name='search'),  # URL for the search view
]
