import pytest
from blog.models import Post


@pytest.mark.django_db
def test_post_creation():
    post = Post.objects.create(title="Test Post", body="Test Body")
    assert post.title == "Test Post"
    assert post.body == "Test Body"
    assert post.slug == "test-post"
    assert post.pk is not None


@pytest.mark.django_db
def test_post_creation_with_ampresand():
    post = Post.objects.create(title="Test&Post", body="Test Body")
    assert post.title == "Test&Post"
    assert post.body == "Test Body"
    assert post.slug == "test-and-post"
    assert post.pk is not None


@pytest.mark.django_db
def test_unique_slug_generation():
    post1 = Post.objects.create(title="Duplicate Title")
    post2 = Post.objects.create(title="Duplicate Title")

    assert post1.slug != post2.slug


@pytest.mark.django_db
def test_provided_slug_is_used():
    custom_slug = "custom-slug"
    post = Post.objects.create(title="Some Title", slug=custom_slug)

    assert post.slug == custom_slug
