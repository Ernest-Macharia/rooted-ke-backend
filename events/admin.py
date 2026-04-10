from django.contrib import admin
from .models import Event, EventBooking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'destination', 'start_date', 'price', 'is_featured']
    list_filter = ['category', 'destination', 'is_featured', 'start_date']
    search_fields = ['title', 'short', 'description', 'venue', 'area']
    prepopulated_fields = {'slug': ['title']}
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short', 'description', 'category')
        }),
        ('Location & Timing', {
            'fields': ('destination', 'venue', 'area', 'address', 'start_date', 'end_date', 'time_display')
        }),
        ('Pricing', {
            'fields': ('price', 'price_display', 'capacity')
        }),
        ('Media', {
            'fields': ('image', 'image_url', 'gallery')
        }),
        ('Frontend Details', {
            'fields': ('lineup', 'tips', 'tags', 'ticket_link', 'what_to_pair')
        }),
        ('Featured', {
            'fields': ('is_featured',)
        }),
    )

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'tickets', 'booking_date']
    list_filter = ['event', 'booking_date']
    search_fields = ['name', 'email']
