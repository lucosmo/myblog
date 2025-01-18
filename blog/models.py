from django.db import models
from html import escape

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    author = models.CharField(max_length=60)
    email = models.EmailField(max_length=150)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(protocol='both', null=False, blank=False)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
    active = models.BooleanField(default=False)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"
    
    def save(self, *args, **kwargs):
        self.author = escape(self.author)
        self.body = escape(self.body)
        self.email = escape(self.email)
        self.user_agent = escape(self.user_agent)
        self.referrer = escape(self.referrer)

        super().save(*args, **kwargs)