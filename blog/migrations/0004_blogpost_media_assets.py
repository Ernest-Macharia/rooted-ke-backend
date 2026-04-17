from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost_author_avatar'),
        ('core', '0005_mediaasset'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='author_avatar_media_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_author_avatars', to='core.mediaasset'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='featured_media_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_posts', to='core.mediaasset'),
        ),
    ]
