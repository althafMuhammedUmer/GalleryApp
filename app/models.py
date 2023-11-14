from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

    
class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image =  models.ImageField(upload_to='images/')
    tags = models.ManyToManyField(Tag, blank=True)
    caption = models.CharField(max_length=55, blank=True)

    saved_by = models.ManyToManyField(CustomUser, related_name='saved_posts', blank=True)
    liked_by = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Post - {self.created_at}"
    

class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.caption}"





