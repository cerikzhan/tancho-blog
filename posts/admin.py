from django.contrib import admin

from .models import Category, Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created')

admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)
