from django.db.models.signals import pre_save
from django.dispatch import receiver, Signal

from .models import Post
from blog.utils import slugify

views_signal = Signal(providing_args=['instance', 'request'])


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    if qs.exists():
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Post)
def post_slug_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

@receiver(views_signal)
def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    instance.views += 1
    instance.save()
