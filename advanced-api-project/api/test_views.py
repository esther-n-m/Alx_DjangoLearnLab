
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .models import Author, Book

User = get_user_model()


class BookAPITests(APITestCase):
    def setUp(self):
        # Users
        self.user = User.objects.create_user(username="tester", password="pass12345")

        # Data
        self.author1 = Author.objects.create(name="Chinua Achebe")
        self.author2 = Author.objects.create(name="Robert C. Martin")

        self.book1 = Book.objects.create(
            title="Things Fall Apart", publication_year=1958, author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Clean Code", publication_year=2008, author=self.author2
        )
        self.book3 = Book.objects.create(
            title="Clean Architecture", publication_year=2017, author=self.author2
        )

        # Common URLs (names must match your api/urls.py)
        self.list_url = reverse("book-list")                # /api/books/
        self.detail_url = reverse("book-detail", args=[self.book1.pk])  # /api/books/<pk>/
        self.create_url = reverse("book-create")            # /api/books/create/
        self.update_url = reverse("book-update", args=[self.book2.pk])  # /api/books/update/<pk>/
        self.delete_url = reverse("book-delete", args=[self.book3.pk])  # /api/books/delete/<pk>/

    # ---------- READ (no auth required with IsAuthenticatedOrReadOnly) ----------
    def test_list_books_unauthenticated_ok(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 2)
        titles = [b["title"] for b in res.data]
        self.assertIn("Things Fall Apart", titles)

    def test_retrieve_book_unauthenticated_ok(self):
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "Things Fall Apart")
        self.assertEqual(res.data["publication_year"], 1958)

    # ---------- CREATE (auth required) ----------
    def test_create_book_requires_auth(self):
        payload = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author1.id,
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "The Pragmatic Programmer",
            "publication_year": 1999,
            "author": self.author2.id,
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="The Pragmatic Programmer").exists())

    def test_create_book_future_year_validation(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Future Book",
            "publication_year": timezone.now().year + 5,  # invalid
            "author": self.author1.id,
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", res.data)

    # ---------- UPDATE (auth required) ----------
    def test_update_book_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Clean Code (Updated)",
            "publication_year": 2008,
            "author": self.author2.id,
        }
        res = self.client.put(self.update_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, "Clean Code (Updated)")

    # ---------- DELETE (auth required) ----------
    def test_delete_book_authenticated_success(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(self.delete_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book3.pk).exists())

    # ---------- FILTER / SEARCH / ORDER ----------
    def test_filter_by_publication_year(self):
        res = self.client.get(self.list_url, {"publication_year": 2008})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(all(b["publication_year"] == 2008 for b in res.data))

    def test_filter_by_author_name(self):
        res = self.client.get(self.list_url, {"author__name": "Robert C. Martin"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertIn("Clean Code", titles)
        self.assertIn("Clean Architecture", titles)

    def test_search_by_title(self):
        res = self.client.get(self.list_url, {"search": "Clean"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertIn("Clean Code", titles)
        self.assertIn("Clean Architecture", titles)

    def test_ordering_by_publication_year_desc(self):
        res = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in res.data]
        self.assertEqual(years, sorted(years, reverse=True))
