from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_author_avatar_url_blogpost_body_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='author_avatar',
            field=models.ImageField(blank=True, null=True, upload_to='blog/authors/'),
        ),
    ]
