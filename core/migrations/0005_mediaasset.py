from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_homepage_full_cms_and_feature_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media-library/')),
                ('image_url', models.URLField(blank=True)),
                ('alt_text', models.CharField(blank=True, max_length=255)),
                ('tags', models.CharField(blank=True, help_text='Comma-separated tags', max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Media Asset',
                'verbose_name_plural': 'Media Library',
                'ordering': ['title', '-created_at'],
            },
        ),
    ]
