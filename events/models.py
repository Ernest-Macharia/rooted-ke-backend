from django.db import models
from django.utils.text import slugify
from destinations.models import Destination

class Event(models.Model):
    EVENT_CATEGORIES = [
        ('this_weekend', 'This Weekend'),
        ('concerts', 'Concerts & Festivals'),
        ('nightlife', 'Nightlife & Parties'),
        ('cultural', 'Cultural & Pop-Ups'),
        ('sports', 'Sports & Outdoor'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=20, choices=EVENT_CATEGORIES)
    destination = models.ForeignKey(Destination, related_name='events', on_delete=models.CASCADE)
    venue = models.CharField(max_length=200)
    area = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=300)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_display = models.CharField(max_length=120, blank=True)
    time_display = models.CharField(max_length=120, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    image_url = models.URLField(blank=True)
    lineup = models.JSONField(default=list, blank=True)
    tips = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    gallery = models.JSONField(default=list, blank=True)
    ticket_link = models.URLField(blank=True)
    what_to_pair = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_date']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class EventBooking(models.Model):
    event = models.ForeignKey(Event, related_name='bookings', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    tickets = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"
