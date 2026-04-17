from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_mediaasset'),
        ('destinations', '0003_destination_card_hero_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='card_media_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destination_card_items', to='core.mediaasset'),
        ),
        migrations.AddField(
            model_name='destination',
            name='hero_media_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destination_hero_items', to='core.mediaasset'),
        ),
        migrations.AddField(
            model_name='destinationimage',
            name='media_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destination_images', to='core.mediaasset'),
        ),
    ]
