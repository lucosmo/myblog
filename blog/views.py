import os
import uuid
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.html import escape
from django.shortcuts import render, get_object_or_404
from django.core.cache import cache
from blog.models import Post, Comment, Category, SiteStats
from django.views.decorators.csrf import csrf_protect
from blog.forms import CommentForm
from blog.utils import get_client_ip
from PIL import Image
from io import BytesIO


def create_side_column_context():
    posts = Post.objects.all().order_by("-created_on")
    categories = Category.objects.all()
    recent_posts = Post.objects.all().order_by("-created_on")[:5]
    popular_posts = Post.objects.filter(popular=True).order_by("-total_views")[:5]

    context = {
        "posts": posts,
        "categories": categories,
        "recent_posts": recent_posts,
        "popular_posts": popular_posts,
    }
    return context


@csrf_protect
def blog_index(request):
    if not request.session.get('visited_homepage'):
        stats, created = SiteStats.objects.get_or_create(pk=1)
        stats.homepage_unique_views += 1
        stats.save()
        request.session['visited_homepage'] = True

    homepage_total_key = 'homepage_total_views'
    if cache.get(homepage_total_key) is None:
        cache.set(homepage_total_key, 0)
    try:
        cache.incr(homepage_total_key)
    except ValueError:
        current = cache.get(homepage_total_key)
        cache.set(homepage_total_key, current + 1)

    context = create_side_column_context()
    return render(request, "blog/index.html", context)


@csrf_protect
def blog_category(request, category):
    safe_category = escape(category)
    posts = Post.objects.filter(categories__name__contains=safe_category).order_by(
        "-created_on"
    )
    context = {
        "category": safe_category,
        "posts": posts,
    }
    side_column_context = create_side_column_context()
    side_column_context.pop("posts")
    context.update(side_column_context)
    return render(request, "blog/category.html", context)


@csrf_protect
def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                email=form.cleaned_data["email"],
                ip=get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                referrer=request.META.get("HTTP_REFERER", ""),
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    visited_posts = request.session.get('visited_posts', [])
    if post.pk not in visited_posts:
        post.unique_views += 1
        visited_posts.append(post.pk)
        request.session['visited_posts'] = visited_posts
        post.save()

    post_total_key = f'post_total_views_{post.pk}'
    if cache.get(post_total_key) is None:
        cache.set(post_total_key, 0)
    try:
        cache.incr(post_total_key)
    except ValueError:
        current = cache.get(post_total_key)
        cache.set(post_total_key, current + 1)

    comments = Comment.objects.filter(post=post, active=True)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    side_column_context = create_side_column_context()
    context.update(side_column_context)
    return render(request, "blog/detail.html", context)


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        image = request.FILES.get("file")
        if image:
            extension = os.path.splitext(image.name)[1]
            random_filename = f"{uuid.uuid4().hex}{extension}"

            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, random_filename)

            try:
                img = Image.open(image)
                img.thumbnail((800, 800))

                buffer = BytesIO()
                img.save(buffer, format=img.format)
                buffer.seek(0)

                with open(file_path, "wb+") as destination:
                    destination.write(buffer.read())

                file_url = f"{settings.MEDIA_URL}uploads/{random_filename}"

                return JsonResponse({"location": file_url})
            except Exception as e:
                return JsonResponse(
                    {"error": f"Error processing image: {str(e)}"}, status=500
                )

        return JsonResponse({"error": "No file uploaded"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)
