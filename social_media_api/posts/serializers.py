from rest_framework import serializers
from .models import Post, Like

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author", "author_username", "content", "created_at", "likes_count"]
        read_only_fields = ["id", "author", "author_username", "created_at", "likes_count"]

