import pytest
from blog.models import Post


@pytest.mark.django_db
def test_post_creation():
    post = Post.objects.create(title="Test Post", body="Test Body")
    assert post.title == "Test Post"
    assert post.body == "Test Body"
    assert post.pk is not None
