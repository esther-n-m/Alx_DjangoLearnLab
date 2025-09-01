from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Represents an author with a name.
    Each Author can have multiple related Book entries.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book written by an Author.
    Linked to Author via a foreign key (One-to-Many relationship).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
