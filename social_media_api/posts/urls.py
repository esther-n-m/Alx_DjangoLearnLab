from django.urls import path
from .views import FeedView , LikePostView, UnlikePostView , PostListCreateView, PostDetailView

urlpatterns = [
    path("feed/", FeedView.as_view(), name="feed"),
    
    path("<int:pk>/unlike/", UnlikePostView.as_view(), name="unlike-post"),
    path("", PostListCreateView.as_view(), name="post-list-create"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:pk>/like/", LikePostView.as_view(), name="post-like"), 
    
]
