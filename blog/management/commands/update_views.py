from django.core.management.base import BaseCommand
from django.core.cache import cache
from blog.models import Post, SiteStats

class Command(BaseCommand):
    help = 'Sync counter from cache to db'

    def handle(self, *args, **options):
        
        homepage_total_key = 'homepage_total_views'
        total_homepage_views = cache.get(homepage_total_key, 0)
        if total_homepage_views:
            stats, created = SiteStats.objects.get_or_create(pk=1)
            stats.homepage_total_views += int(total_homepage_views)
            stats.save()
            cache.set(homepage_total_key, 0)
            self.stdout.write(f"homepage total views updated by {total_homepage_views}")

        posts = Post.objects.all()
        for post in posts:
            post_total_key = f'post_total_views_{post.pk}'
            total_post_views = cache.get(post_total_key, 0)
            if total_post_views:
                post.total_views += int(total_post_views)
                post.save()
                cache.set(post_total_key, 0)
                self.stdout.write(f"post views updated by {post.pk} o {total_post_views}")
