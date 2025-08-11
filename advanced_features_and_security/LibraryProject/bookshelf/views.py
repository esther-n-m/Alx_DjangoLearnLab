from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required('bookshelf.can_view')
def view_books(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/view_books.html', {'books': books})

@permission_required('bookshelf.can_create')
def create_book(request):
    # Logic to create book
    return render(request, 'bookshelf/create_book.html')

@permission_required('bookshelf.can_edit')
def edit_book(request, book_id):
    # Logic to edit book
    return render(request, 'bookshelf/edit_book.html')

@permission_required('bookshelf.can_delete')
def delete_book(request, book_id):
    # Logic to delete book
    return render(request, 'bookshelf/delete_book.html')
