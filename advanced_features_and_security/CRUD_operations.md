## CREATE
from bookshelf.models import Book

book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

book
# Output: <Book: 1984>

## RETRIEVE
from bookshelf.models import Book

my_book = Book.objects.get(title="1984")
my_book.title, my_book.author, my_book.publication_year
# Output: ('1984', 'George Orwell', 1949)

## UPDATE
my_book = Book.objects.get(title="1984")
my_book.title = "Nineteen Eighty-Four"
my_book.save()

my_book.title
# Output: 'Nineteen Eighty-Four'

## DELETE
my_book = Book.objects.get(title="Nineteen Eighty-Four")
my_book.delete()
# Output: (1, {'bookshelf.Book': 1})

Book.objects.all()
# Output: <QuerySet []>
