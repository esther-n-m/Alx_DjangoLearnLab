from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, profile
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView
)

from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView , CommentUpdateView, CommentDeleteView
from .views import CommentCreateView

urlpatterns = [
    # Auth
    path("login/",  auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logged_out.html"), name="logout"),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/new/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post-edit"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment-edit"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
    path("posts/<int:post_id>/comments/new/", CommentCreateView.as_view(), name="comment-create"),
     path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('search/', views.search_posts, name='search-posts'),
    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts-by-tag'),
]
