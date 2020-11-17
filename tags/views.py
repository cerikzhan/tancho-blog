from django.shortcuts import render
from django.views.generic import ListView

from posts.models import Post
from .models import Tag

class TagPostsListView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        qs = Post.objects.filter(tag__slug=self.kwargs['tag_slug']).order_by('-created')
        return qs
