import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"No author named {author_name}")

def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        print(f"Books in library '{library_name}':")
        for book in library.books.all():
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"No library named {library_name}")

def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for library '{library_name}': {librarian.name}")
    except Library.DoesNotExist:
        print(f"No library named {library_name}")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned for library '{library_name}'")

if __name__ == "__main__":
    # Replace the names below with actual data after you create entries
    query_books_by_author("Author Name")
    list_books_in_library("Library Name")
    get_librarian_for_library("Library Name")
