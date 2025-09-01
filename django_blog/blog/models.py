from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.urls import reverse

def get_absolute_url(self):
        return reverse("post-detail", args=[self.pk])
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    tags = TaggableManager() 

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post-detail", args=[self.pk])


class Tag(models.Model):  
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    
class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # when created
    updated_at = models.DateTimeField(auto_now=True)      # last edit

    class Meta:
        ordering = ["-created_at"]  # newest first

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"