from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_homepagesettings_sitepage_sections'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagesettings',
            name='blog_cta_label',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='blog_eyebrow',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='blog_subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='blog_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='destinations_fallback_card_image',
            field=models.ImageField(blank=True, null=True, upload_to='homepage/'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='events_eyebrow',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='events_subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='events_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='hero_background_image',
            field=models.ImageField(blank=True, null=True, upload_to='homepage/'),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='newsletter_button_label',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='newsletter_description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='newsletter_disclaimer',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='newsletter_eyebrow',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='newsletter_subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='newsletter_success_message',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='newsletter_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='packages_eyebrow',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='packages_subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='packages_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='packages_title_emphasis',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='restaurants_eyebrow',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='restaurants_subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='restaurants_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='top_categories_eyebrow',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='top_categories_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='trending_eyebrow',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='trending_subtitle',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='homepagesettings',
            name='trending_title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.CreateModel(
            name='HomePageFeatureItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(choices=[('top_primary', 'Top Categories - Primary Row'), ('top_secondary', 'Top Categories - Secondary Row'), ('trending', 'Trending Cards')], max_length=24)),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='homepage/cards/')),
                ('image_url', models.URLField(blank=True)),
                ('cta_label', models.CharField(blank=True, max_length=80)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('homepage_settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_items', to='core.homepagesettings')),
            ],
            options={
                'ordering': ['section', 'sort_order', 'id'],
            },
        ),
    ]
