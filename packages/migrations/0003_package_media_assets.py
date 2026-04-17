from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_mediaasset'),
        ('packages', '0002_package_best_for_package_card_image_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='card_media_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='package_card_items', to='core.mediaasset'),
        ),
        migrations.AddField(
            model_name='package',
            name='gallery_assets',
            field=models.ManyToManyField(blank=True, related_name='package_galleries', to='core.mediaasset'),
        ),
        migrations.AddField(
            model_name='package',
            name='hero_media_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='package_hero_items', to='core.mediaasset'),
        ),
        migrations.AddField(
            model_name='package',
            name='image_media_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='packages', to='core.mediaasset'),
        ),
    ]
