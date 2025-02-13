from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<slug:category_slug>/", views.blog_category, name="blog_category"),
    path("upload/image/", views.upload_image, name="upload_image"),
]
