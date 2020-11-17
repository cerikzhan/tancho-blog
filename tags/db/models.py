from django.db import models

from posts.models import Post

class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.title
