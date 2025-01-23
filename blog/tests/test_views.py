import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from blog.models import Post
from PIL import Image
from io import BytesIO


@pytest.fixture(autouse=True)
def setup_media_root(tmpdir, settings):
    settings.MEDIA_ROOT = tmpdir.mkdir("media")


@pytest.mark.django_db
def test_upload_image_success(client):
    url = reverse("upload_image")

    image = Image.new("RGB", (100, 100), color="red")
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    image_content = SimpleUploadedFile(
        "test_image.jpg", buffer.read(), content_type="image/jpeg"
    )

    response = client.post(url, {"file": image_content})
    print(response.content)
    assert response.status_code == 200
    response_data = response.json()
    assert "location" in response_data
    assert response_data["location"].startswith(settings.MEDIA_URL)


@pytest.mark.django_db
def test_upload_image_no_file(client):
    url = reverse("upload_image")
    response = client.post(url, {})
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["error"] == "No file uploaded"


@pytest.mark.django_db
def test_post_detail_rendering(client):
    post = Post.objects.create(
        title="Test Post",
        body=(
            "<pre class='line-numbers'><code class='language-python'>"
            "print('Hello, world!')</code></pre>"
        ),
    )
    url = reverse("blog_detail", args=[post.pk])
    response = client.get(url)

    assert response.status_code == 200
    assert "<pre class='line-numbers'>" in response.content.decode()
    assert "class='language-python'" in response.content.decode()
