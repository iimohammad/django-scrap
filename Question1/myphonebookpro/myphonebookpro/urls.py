from django.contrib import admin
from django.urls import path, include
from myphonebookpro import local_settings

urlpatterns = [
    path(local_settings.Admin_Settings['admin'], admin.site.urls),
    path('phonebook/', include('contacts.urls')),
]
