from django.db import models
from django.db.models import Q

class PostQuerySet(models.QuerySet):
    def related_posts(self, post_id, category):
        posts = self.exclude(id=post_id).filter(category=category).order_by('?')
        if posts.count() >= 2:
            return posts[:2]
        return posts

    def search(self, query):
        lookups = (
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(tag__title__icontains=query)
        )
        return self.filter(lookups).distinct()

class PostManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PostQuerySet(self.model, using=self._db)

    def related_posts(self, post_id, category):
        return self.get_queryset().related_posts(post_id, category)

    def search(self, query):
        return self.get_queryset().search(query)