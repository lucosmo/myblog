import pytest
from django.contrib.admin.sites import site
from blog.models import Post
from django.test import RequestFactory
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_tinymce_in_admin():
    factory = RequestFactory()
    request = factory.get("/")
    request.user = User.objects.create_superuser(
        "admin", "admin@example.com", "password"
    )

    admin_form = site._registry[Post].get_form(request)
    form = admin_form()
    from tinymce.widgets import TinyMCE

    assert isinstance(form.base_fields["body"].widget, TinyMCE)
