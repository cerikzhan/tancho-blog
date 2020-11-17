from django.urls import path, include

from .views import inactive_comments, delete_comment

urlpatterns = [
    path("inactive/", inactive_comments, name='inactive'),
    path("delete-comment/", delete_comment, name='delete-comment'),
]