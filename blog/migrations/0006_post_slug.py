from django.db import migrations, models
from django.utils.text import slugify

def generate_unique_slug(post_instance, Post):
    base_slug = slugify(post_instance.title.replace("&", " and "))
    unique_slug = base_slug
    counter = 1

    while Post.objects.filter(slug=unique_slug).exclude(id=post_instance.id).exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1

    return unique_slug

def generate_slugs(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    for post in Post.objects.all():
        if not post.slug or Post.objects.filter(slug=post.slug).exclude(id=post.id).exists():
            post.slug = generate_unique_slug(post, Post)
            post.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_update_slugs'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=255, blank=True, null=True),
        ),
        migrations.RunPython(generate_slugs),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]