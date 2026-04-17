from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_mediaasset'),
        ('restaurants', '0002_restaurant_area_restaurant_best_for_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='gallery_assets',
            field=models.ManyToManyField(blank=True, related_name='restaurant_galleries', to='core.mediaasset'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='media_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='restaurants', to='core.mediaasset'),
        ),
    ]
