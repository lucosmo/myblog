from django.contrib import admin
from django import forms
from blog.models import Category, Comment, Post
from tinymce.widgets import TinyMCE


class CategoryAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    body = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))

    class Meta:
        model = Post
        fields = "__all__"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "email", "created_on", "active")
    list_filter = ("active", "created_on")
    search_fields = ("author", "email", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

    approve_comments.short_description = "Approve selected comments"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
