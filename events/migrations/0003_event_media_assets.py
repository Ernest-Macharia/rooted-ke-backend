from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_mediaasset'),
        ('events', '0002_event_area_event_gallery_event_image_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='gallery_assets',
            field=models.ManyToManyField(blank=True, related_name='event_galleries', to='core.mediaasset'),
        ),
        migrations.AddField(
            model_name='event',
            name='media_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='core.mediaasset'),
        ),
    ]
