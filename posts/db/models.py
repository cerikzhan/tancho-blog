from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .managers import *

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg")
    content = models.TextField()
    views = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug, "cat_slug": self.category.slug})

    @property
    def previous_post(self):
        previous = self.get_previous_by_created()
        if previous:
            return previous
        return None

    @property
    def next_post(self):
        next_p = self.get_next_by_created()
        if next_p:
            return next_p
        return None

    @property
    def comments(self):
        return self.comment_set.active_comments(post=self)

    @property
    def inactive_comments(self):
        return self.comment_set.inactive_comments(post=self)

    @property
    def tags(self):
        return self.tag_set.all()
