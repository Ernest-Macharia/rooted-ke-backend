from django.db import models
from django.utils.text import slugify
from destinations.models import Destination

class Cuisine(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    BUDGET_TIERS = [
        ('budget', 'Budget (under 500 KES)'),
        ('mid', 'Mid-range (500-1500 KES)'),
        ('luxury', 'Luxury (1500+ KES)'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    destination = models.ForeignKey(Destination, related_name='restaurants', on_delete=models.CASCADE)
    cuisine = models.ManyToManyField(Cuisine, related_name='restaurants')
    budget_tier = models.CharField(max_length=10, choices=BUDGET_TIERS)
    budget_label = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=300)
    area = models.CharField(max_length=200, blank=True)
    price_range = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    opening_hours = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    image = models.ImageField(upload_to='restaurants/', null=True, blank=True)
    image_url = models.URLField(blank=True)
    media_asset = models.ForeignKey('core.MediaAsset', null=True, blank=True, on_delete=models.SET_NULL, related_name='restaurants')
    best_for = models.JSONField(default=list, blank=True)
    must_order = models.JSONField(default=list, blank=True)
    booking_required = models.BooleanField(default=False)
    location_label = models.CharField(max_length=300, blank=True)
    tags = models.JSONField(default=list, blank=True)
    gallery = models.JSONField(default=list, blank=True)
    gallery_assets = models.ManyToManyField('core.MediaAsset', related_name='restaurant_galleries', blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-rating']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.rating}★"
