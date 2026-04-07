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
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ['name']}
    filter_horizontal = ['destinations', 'gallery']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category', 'image')
        }),
        ('Duration', {
            'fields': ('duration_days', 'duration_nights')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price')
        }),
        ('Content', {
            'fields': ('includes', 'excludes', 'itinerary')
        }),
        ('Featured', {
            'fields': ('is_featured',)
        }),
    )

@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption']