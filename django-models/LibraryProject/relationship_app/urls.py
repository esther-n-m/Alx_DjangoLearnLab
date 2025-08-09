from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import add_book, edit_book, delete_book



urlpatterns = [
    path('books/', views.list_books, name='list_books'),  # FBV URL
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # CBV URL
    
    # Authentication URLs using built-in class-based views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Registration is custom, so keep your function view
    path('register/', views.register, name='register'),
    
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
    
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', delete_book, name='delete_book'),
]
