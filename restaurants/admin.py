from django.contrib import admin
from django import forms

from core.admin_json_fields import JsonStringListFormField
from .models import Restaurant, Cuisine, RestaurantReview

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    class RestaurantAdminForm(forms.ModelForm):
        best_for = JsonStringListFormField(help_text='Enter one item per line.')
        must_order = JsonStringListFormField(help_text='Enter one dish per line.')
        tags = JsonStringListFormField(help_text='Enter one tag per line.')
        gallery = JsonStringListFormField(help_text='Enter one image URL per line.')

        class Meta:
            model = Restaurant
            fields = '__all__'

    form = RestaurantAdminForm
    list_display = ['name', 'destination', 'budget_tier', 'rating', 'is_featured']
    list_filter = ['budget_tier', 'cuisine', 'destination', 'is_featured']
    search_fields = ['name', 'short', 'description', 'address', 'area']
    prepopulated_fields = {'slug': ['name']}
    filter_horizontal = ['cuisine', 'gallery_assets']
    autocomplete_fields = ['media_asset', 'destination']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'short', 'description', 'destination', 'cuisine')
        }),
        ('Pricing & Classification', {
            'fields': ('budget_tier', 'budget_label', 'price_range', 'rating')
        }),
        ('Contact & Location', {
            'fields': ('address', 'area', 'location_label', 'phone', 'email', 'website', 'opening_hours')
        }),
        ('Media & Frontend Content', {
            'fields': ('image', 'image_url', 'media_asset', 'gallery_assets', 'gallery', 'best_for', 'must_order', 'tags')
        }),
        ('Booking', {
            'fields': ('booking_required', 'is_featured')
        }),
    )

@admin.register(RestaurantReview)
class RestaurantReviewAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
