from django.db import migrations, models


def copy_sections_from_json(apps, schema_editor):
    SitePage = apps.get_model('core', 'SitePage')
    for page in SitePage.objects.all():
        content = page.content or {}
        sections = content.get('sections') if isinstance(content, dict) else None
        if not isinstance(sections, list):
            continue

        pairs = []
        for section in sections:
            if not isinstance(section, dict):
                continue
            heading = section.get('heading')
            text = section.get('text')
            if isinstance(heading, str) and isinstance(text, str):
                pairs.append((heading, text))

        if len(pairs) > 0 and not page.section_1_heading and not page.section_1_body:
            page.section_1_heading, page.section_1_body = pairs[0]
        if len(pairs) > 1 and not page.section_2_heading and not page.section_2_body:
            page.section_2_heading, page.section_2_body = pairs[1]
        if len(pairs) > 2 and not page.section_3_heading and not page.section_3_body:
            page.section_3_heading, page.section_3_body = pairs[2]

        page.save(update_fields=[
            'section_1_heading', 'section_1_body',
            'section_2_heading', 'section_2_body',
            'section_3_heading', 'section_3_body',
        ])


def noop_reverse(apps, schema_editor):
    return


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_sitepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitepage',
            name='section_1_body',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='sitepage',
            name='section_1_heading',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='sitepage',
            name='section_2_body',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='sitepage',
            name='section_2_heading',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='sitepage',
            name='section_3_body',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='sitepage',
            name='section_3_heading',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.CreateModel(
            name='HomePageSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('singleton_key', models.CharField(default='default', max_length=32, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('hero_eyebrow', models.CharField(blank=True, max_length=120)),
                ('hero_title', models.CharField(blank=True, max_length=200)),
                ('hero_subtitle', models.CharField(blank=True, max_length=200)),
                ('hero_description', models.TextField(blank=True)),
                ('hero_background_image_url', models.URLField(blank=True)),
                ('destinations_eyebrow', models.CharField(blank=True, max_length=120)),
                ('destinations_title', models.CharField(blank=True, max_length=200)),
                ('destinations_subtitle', models.CharField(blank=True, max_length=255)),
                ('destinations_fallback_card_image_url', models.URLField(blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Homepage Settings',
                'verbose_name_plural': 'Homepage Settings',
            },
        ),
        migrations.RunPython(copy_sections_from_json, noop_reverse),
    ]
