# forms.py
from django import forms


class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search')
    max_pages = forms.IntegerField(label='Max Page')
