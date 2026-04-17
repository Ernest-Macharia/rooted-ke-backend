from django.db import models


class MediaAsset(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media-library/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text='Comma-separated tags')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title', '-created_at']
        verbose_name = 'Media Asset'
        verbose_name_plural = 'Media Library'

    def __str__(self):
        return self.title


class ContentBlock(models.Model):
    """
    Generic CMS block for frontend-managed content.
    Use `key` to store things like:
    - navigation
    - homepage
    - footer
    - restaurant_filters
    - event_categories
    """

    key = models.SlugField(unique=True, max_length=120)
    title = models.CharField(max_length=200)
    content = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["key"]

    def __str__(self):
        return f"{self.key}: {self.title}"


class SitePage(models.Model):
    """
    Admin-managed static pages (About, Contact, Privacy Policy, Terms of Service).
    Frontend should fetch by slug.
    """

    slug = models.SlugField(unique=True, max_length=120)
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    # Deprecated for frontend rendering. Kept for backwards compatibility.
    content = models.JSONField(default=dict, blank=True)
    section_1_heading = models.CharField(max_length=200, blank=True)
    section_1_body = models.TextField(blank=True)
    section_2_heading = models.CharField(max_length=200, blank=True)
    section_2_body = models.TextField(blank=True)
    section_3_heading = models.CharField(max_length=200, blank=True)
    section_3_body = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return f"{self.slug}: {self.title}"


class HomePageSettings(models.Model):
    """
    Non-technical CMS fields for homepage content.
    """

    singleton_key = models.CharField(max_length=32, unique=True, default="default")
    is_active = models.BooleanField(default=True)

    hero_eyebrow = models.CharField(max_length=120, blank=True)
    hero_title = models.CharField(max_length=200, blank=True)
    hero_subtitle = models.CharField(max_length=200, blank=True)
    hero_description = models.TextField(blank=True)
    hero_background_image = models.ImageField(upload_to='homepage/', blank=True, null=True)
    hero_background_image_url = models.URLField(blank=True)

    destinations_eyebrow = models.CharField(max_length=120, blank=True)
    destinations_title = models.CharField(max_length=200, blank=True)
    destinations_subtitle = models.CharField(max_length=255, blank=True)
    destinations_fallback_card_image = models.ImageField(upload_to='homepage/', blank=True, null=True)
    destinations_fallback_card_image_url = models.URLField(blank=True)

    top_categories_eyebrow = models.CharField(max_length=120, blank=True)
    top_categories_title = models.CharField(max_length=200, blank=True)

    trending_eyebrow = models.CharField(max_length=120, blank=True)
    trending_title = models.CharField(max_length=200, blank=True)
    trending_subtitle = models.CharField(max_length=255, blank=True)

    restaurants_eyebrow = models.CharField(max_length=120, blank=True)
    restaurants_title = models.CharField(max_length=200, blank=True)
    restaurants_subtitle = models.CharField(max_length=255, blank=True)

    events_eyebrow = models.CharField(max_length=120, blank=True)
    events_title = models.CharField(max_length=200, blank=True)
    events_subtitle = models.CharField(max_length=255, blank=True)

    packages_eyebrow = models.CharField(max_length=120, blank=True)
    packages_title = models.CharField(max_length=200, blank=True)
    packages_title_emphasis = models.CharField(max_length=120, blank=True)
    packages_subtitle = models.CharField(max_length=255, blank=True)

    blog_eyebrow = models.CharField(max_length=120, blank=True)
    blog_title = models.CharField(max_length=200, blank=True)
    blog_subtitle = models.CharField(max_length=255, blank=True)
    blog_cta_label = models.CharField(max_length=80, blank=True)

    newsletter_eyebrow = models.CharField(max_length=120, blank=True)
    newsletter_title = models.CharField(max_length=200, blank=True)
    newsletter_subtitle = models.CharField(max_length=255, blank=True)
    newsletter_description = models.CharField(max_length=255, blank=True)
    newsletter_disclaimer = models.CharField(max_length=255, blank=True)
    newsletter_button_label = models.CharField(max_length=80, blank=True)
    newsletter_success_message = models.CharField(max_length=255, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Homepage Settings"
        verbose_name_plural = "Homepage Settings"

    def __str__(self):
        return "Homepage Settings"


class HomePageFeatureItem(models.Model):
    SECTION_CHOICES = [
        ('top_primary', 'Top Categories - Primary Row'),
        ('top_secondary', 'Top Categories - Secondary Row'),
        ('trending', 'Trending Cards'),
    ]

    homepage_settings = models.ForeignKey(HomePageSettings, related_name='feature_items', on_delete=models.CASCADE)
    section = models.CharField(max_length=24, choices=SECTION_CHOICES)
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    image = models.ImageField(upload_to='homepage/cards/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    cta_label = models.CharField(max_length=80, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['section', 'sort_order', 'id']

    def __str__(self):
        return f"{self.get_section_display()}: {self.title}"
