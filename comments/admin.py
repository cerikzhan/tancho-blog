from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'parent', 'is_active')

admin.site.register(Comment, CommentAdmin)
