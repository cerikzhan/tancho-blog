from django.urls import path

from .views import (CategoryListView, 
                    PostListView, 
                    PostDetailView, 
                    PostCreateView, 
                    PostUpdateView,
                    PostDeleteView,
                    )

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path("posts/<str:cat_slug>/", CategoryListView.as_view(), name="category"),
    path("posts/<str:cat_slug>/<str:slug>/", PostDetailView.as_view(), name="post-detail"),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path("posts/<str:cat_slug>/<str:slug>/update", PostUpdateView.as_view(), name="post-update"),
    path("posts/<str:cat_slug>/<str:slug>/delete", PostDeleteView.as_view(), name="post-delete"),
]
