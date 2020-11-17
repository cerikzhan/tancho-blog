from django.db import models

class CommentQuerySet(models.QuerySet):
    def inactive(self):
        return self.filter(is_active=False)

    def active(self):
        return self.filter(is_active=True)

    def active_comments(self, post):
        return self.filter(post=post, is_active=True, parent=None)

    def inactive_comments(self, post):
        return self.filter(post=post, is_active=False, parent=None)


class CommentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return CommentQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def active_comments(self, post):
        return self.get_queryset().active_comments(post)

    def inactive_comments(self, post):
        return self.get_queryset().inactive_comments(post)

    def inactive(self):
        return self.get_queryset().inactive()
        
