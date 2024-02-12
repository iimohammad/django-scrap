from django.urls import path
from .views import *

urlpatterns = [
    path('', contact_list),
    path('add/', add_contact, name='add_contact'),
    path('delete/', delete_contact, name='delete_contact'),
    path('search/', search_contact, name='search_contact'),
]