from django.contrib import admin
from .models import Destination, DestinationImage, DestinationTag

class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 1

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'short', 'location', 'price_from', 'rating', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'tags', 'created_at']
    search_fields = ['name', 'short', 'description', 'overview', 'location']
    prepopulated_fields = {'slug': ['name']}
    inlines = [DestinationImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'short', 'description', 'overview', 'location')
        }),
        ('Frontend Content', {
            'fields': ('card_image_url', 'hero_image_url', 'highlights', 'things_to_do', 'display_tags', 'package_link', 'hotel_search')
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
    list_display = ['destination', 'is_primary', 'alt_text', 'image_url']
    list_filter = ['is_primary', 'destination']

@admin.register(DestinationTag)
class DestinationTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}
