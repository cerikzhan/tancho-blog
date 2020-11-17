from django.urls import path, include

from .views import TagPostsListView

urlpatterns = [
    path("<str:tag_slug>/", TagPostsListView.as_view(), name='tag-posts'),
]