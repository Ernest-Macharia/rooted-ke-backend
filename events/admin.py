from django.contrib import admin
from .models import Event, EventBooking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'destination', 'start_date', 'price', 'is_featured']
    list_filter = ['category', 'destination', 'is_featured', 'start_date']
    search_fields = ['title', 'description', 'venue']
    prepopulated_fields = {'slug': ['title']}
    date_hierarchy = 'start_date'

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'tickets', 'booking_date']
    list_filter = ['event', 'booking_date']
    search_fields = ['name', 'email']