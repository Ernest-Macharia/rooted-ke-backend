from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0002_destination_card_image_url_destination_display_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='card_image',
            field=models.ImageField(blank=True, null=True, upload_to='destinations/cards/'),
        ),
        migrations.AddField(
            model_name='destination',
            name='hero_image',
            field=models.ImageField(blank=True, null=True, upload_to='destinations/heroes/'),
        ),
    ]
