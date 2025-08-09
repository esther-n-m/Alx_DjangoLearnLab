
from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # columns shown in list view
    list_filter = ('author', 'publication_year')            # right-side filters
    search_fields = ('title', 'author')                     # search box
    ordering = ('title',)                                   # optional: default ordering

admin.site.register(Book, BookAdmin)
