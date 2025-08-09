my_book = Book.objects.get(title="Nineteen Eighty-Four")
my_book.delete()
# Output: (1, {'bookshelf.Book': 1})

Book.objects.all()
# Output: <QuerySet []>
