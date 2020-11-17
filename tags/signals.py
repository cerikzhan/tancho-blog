from django.db.models.signals import pre_save
from django.dispatch import receiver

from blog.utils import slugify
from .models import Tag

@receiver(pre_save, sender=Tag)
def post_slug_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)