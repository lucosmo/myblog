import pytest
from django.core.management import call_command
from django.core.cache import cache
from blog.models import Post, SiteStats
from io import StringIO

@pytest.mark.django_db
def test_handle(mocker):
    mock_cache = mocker.patch('django.core.cache.cache')
    mock_cache.get.side_effect = lambda key, default=0: {
        'homepage_total_views': 10,
        'post_total_views_1': 5,
        'post_total_views_2': 3,
    }.get(key, default)

    post1 = Post.objects.create(title="Post 1", total_views=0)
    post2 = Post.objects.create(title="Post 2", total_views=0)

    out = StringIO()
    call_command('update_views', stdout=out)

    post1.refresh_from_db()
    post2.refresh_from_db()

    assert post1.total_views == 5
    assert post2.total_views == 3

    stats = SiteStats.objects.get(pk=1)
    assert stats.homepage_total_views == 10

    output = out.getvalue()
    assert 'homepage total views updated by 10' in output
    assert 'post views updated by 1 o 5' in output
    assert 'post views updated by 2 o 3' in output