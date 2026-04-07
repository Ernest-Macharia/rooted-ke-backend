from django.db import models
from django.utils.text import slugify

from destinations.models import Destination


class PackageCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PackageImage(models.Model):
    image = models.ImageField(upload_to='packages/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.caption or f"Package Image {self.pk}"


class Package(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        PackageCategory,
        related_name='packages',
        on_delete=models.CASCADE,
    )
    destinations = models.ManyToManyField(Destination, related_name='packages')
    duration_days = models.PositiveIntegerField()
    duration_nights = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    includes = models.TextField(blank=True)
    excludes = models.TextField(blank=True)
    itinerary = models.TextField(blank=True)
    image = models.ImageField(upload_to='packages/', null=True, blank=True)
    gallery = models.ManyToManyField(
        PackageImage,
        related_name='packages',
        blank=True,
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
