import pytest
from blog.models import Post
from tinymce.widgets import TinyMCE


@pytest.mark.django_db
def test_tinymce_widget_in_form():
    post = Post.objects.create(title="Test Post", body="<p>Test content</p>")
    form_field = post._meta.get_field("body").formfield()
    assert isinstance(form_field.widget, TinyMCE)
