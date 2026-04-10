from django.db import models


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
    content = models.JSONField(default=dict, blank=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return f"{self.slug}: {self.title}"
