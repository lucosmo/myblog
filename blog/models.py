from django.db import models
from html import escape
from tinymce.models import HTMLField
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.replace("&", " and "))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = HTMLField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    popular = models.BooleanField(default=False)
    total_views = models.PositiveIntegerField(default=0)
    unique_views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title.replace("&", " and "))
            unique_slug = base_slug
            counter = 1

            while Post.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=60)
    email = models.EmailField(max_length=150)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(protocol="both", null=False, blank=False)
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


class UploadedImage(models.Model):
    image = models.ImageField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class SiteStats(models.Model):
    homepage_unique_views = models.PositiveIntegerField(default=0)
    homepage_total_views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Main site stats."
