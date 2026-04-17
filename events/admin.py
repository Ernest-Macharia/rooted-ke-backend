from django.contrib import admin
from django import forms

from core.admin_json_fields import JsonStringListFormField
from .models import Event, EventBooking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    class EventAdminForm(forms.ModelForm):
        lineup = JsonStringListFormField(help_text='Enter one performer per line.')
        tips = JsonStringListFormField(help_text='Enter one tip per line.')
        tags = JsonStringListFormField(help_text='Enter one tag per line.')
        gallery = JsonStringListFormField(help_text='Enter one image URL per line.')

        class Meta:
            model = Event
            fields = '__all__'

    form = EventAdminForm
    list_display = ['title', 'category', 'destination', 'start_date', 'price', 'is_featured']
    list_filter = ['category', 'destination', 'is_featured', 'start_date']
    search_fields = ['title', 'short', 'description', 'venue', 'area']
    prepopulated_fields = {'slug': ['title']}
    date_hierarchy = 'start_date'
    filter_horizontal = ['gallery_assets']
    autocomplete_fields = ['media_asset', 'destination']
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
            'fields': ('image', 'image_url', 'media_asset', 'gallery_assets', 'gallery')
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
