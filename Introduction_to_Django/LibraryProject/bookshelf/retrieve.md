from bookshelf.models import Book

my_book = Book.objects.get(title="1984")
my_book.title, my_book.author, my_book.publication_year
# Output: ('1984', 'George Orwell', 1949)
