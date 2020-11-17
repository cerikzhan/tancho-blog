from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect

from comments.forms import CommentForm
from comments.models import Comment
from tags.models import Tag
from .models import Post, Category
from .mixins import ObjectViewMixin

class PostListView(ListView):
    model = Post
    template_name = "posts/index.html"
    context_object_name = "posts"
    ordering = ["-created"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CategoryListView(ListView):
    model = Post    
    template_name = "posts/index.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        qs = Post.objects.filter(category__slug=self.kwargs['cat_slug']).order_by('-created')
        return qs


class PostDetailView(ObjectViewMixin, FormMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = Post.objects.related_posts(post_id=self.object.id, category=self.object.category)
        return context

    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug': self.object.slug, 'cat_slug': self.object.category.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        post = self.get_object()
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        site_url = form.cleaned_data['site_url']
        content = form.cleaned_data['content']
        parent_obj = None
        try:
            parent_id = int(self.request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()

        comment = Comment(
            post=post,
            username=username,
            email=email,
            site_url=site_url,
            content=content, 
            parent=parent_obj,
        )
        comment.save()
        messages.success(self.request, f'Your comment has been created! It shows up after moderation! Thank you!')
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category', 'image', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        post_tags = self.request.POST.get('post_tags')
        if post_tags:
            tags_list = post_tags.split()
            for tag in tags_list:
                tag, _ = Tag.objects.get_or_create(title=tag)
                tag.posts.add(self.object)

        return HttpResponseRedirect(self.get_success_url())


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'category', 'image', 'content']
    template_name = 'posts/post_form.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




