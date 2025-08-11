# Admin configuration for Book model

## Files changed
- `bookshelf/admin.py` — registered Book with a custom ModelAdmin.

## admin.py content
```python
from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')
    ordering = ('title',)

admin.site.register(Book, BookAdmin)
