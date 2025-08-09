my_book = Book.objects.get(title="1984")
my_book.title = "Nineteen Eighty-Four"
my_book.save()

my_book.title
# Output: 'Nineteen Eighty-Four'
