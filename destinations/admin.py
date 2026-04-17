from django.contrib import admin
from django import forms

from core.admin_json_fields import JsonStringListFormField
from .models import Destination, DestinationImage, DestinationTag

class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 1
    autocomplete_fields = ['media_asset']


class DestinationAdminForm(forms.ModelForm):
    highlights = JsonStringListFormField(
        help_text='Enter one item per line. Example: Boutique stays',
    )
    things_to_do = JsonStringListFormField(
        help_text='Enter one activity per line. Example: Game drive',
    )
    display_tags = JsonStringListFormField(
        help_text='Enter one short tag per line. Example: Family friendly',
    )

    class Meta:
        model = Destination
        fields = '__all__'


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    form = DestinationAdminForm
    list_display = ['name', 'short', 'location', 'price_from', 'rating', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'tags', 'created_at']
    search_fields = ['name', 'short', 'description', 'overview', 'location']
    prepopulated_fields = {'slug': ['name']}
    autocomplete_fields = ['card_media_asset', 'hero_media_asset']
    inlines = [DestinationImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'short', 'description', 'overview', 'location')
        }),
        ('Frontend Content', {
            'fields': (
                'card_image', 'card_image_url', 'card_media_asset',
                'hero_image', 'hero_image_url', 'hero_media_asset',
                'highlights', 'things_to_do', 'display_tags', 'package_link', 'hotel_search'
            )
        }),
        ('Location Details', {
            'fields': ('latitude', 'longitude')
        }),
        ('Pricing & Rating', {
            'fields': ('price_from', 'rating')
        }),
        ('Featured', {
            'fields': ('is_featured',)
        }),
    )

@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):
    list_display = ['destination', 'is_primary', 'alt_text', 'image_url', 'media_asset']
    list_filter = ['is_primary', 'destination']
    autocomplete_fields = ['destination', 'media_asset']

@admin.register(DestinationTag)
class DestinationTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}
