from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'average_rating', 'year_published')
    search_fields = ('title', 'author')
    list_filter = ('year_published',)
