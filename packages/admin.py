from django.contrib import admin
from .models import Package, PackageCategory, PackageImage

class PackageImageInline(admin.TabularInline):
    model = Package.gallery.through
    extra = 1

@admin.register(PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'duration_days', 'price', 'discount_price', 'is_featured']
    list_filter = ['category', 'destinations', 'is_featured', 'duration_days']
    search_fields = ['name', 'tagline', 'description', 'overview']
    prepopulated_fields = {'slug': ['name']}
    filter_horizontal = ['destinations', 'gallery']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'tagline', 'description', 'overview', 'category', 'icon', 'image', 'card_image_url', 'hero_image_url')
        }),
        ('Duration', {
            'fields': ('duration_days', 'duration_nights', 'duration')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price')
        }),
        ('Content', {
            'fields': ('includes', 'excludes', 'itinerary', 'best_for', 'inclusions', 'exclusions', 'tiers')
        }),
        ('Frontend Lists', {
            'fields': ('destination_labels', 'gallery_urls')
        }),
        ('Featured', {
            'fields': ('is_featured',)
        }),
    )

@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption']
