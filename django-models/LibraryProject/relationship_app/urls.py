from django.urls import path
from . import views
from .views import list_books, LibraryDetailView ,register
from django.contrib.auth.views import LoginView, LogoutView




urlpatterns = [
    path('books/', views.list_books, name='list_books'),  # FBV URL
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # CBV URL
    
    # Authentication URLs using built-in class-based views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Registration is custom, so keep your function view
    path('register/', register, name='register'),
]
