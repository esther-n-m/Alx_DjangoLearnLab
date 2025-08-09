from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book, Library

# Function-Based View: List all books with authors
def list_books(request):
    books = Book.objects.all()
    return render(request,  'relationship_app/list_books.html', {'books': books})

# Class-Based View: Show detail of one library and its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'  # Template to render
    context_object_name = 'library'        # Context variable in the template
