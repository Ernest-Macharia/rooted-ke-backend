from django.contrib import admin
from django import forms

from core.admin_json_fields import JsonStringListFormField, PackageTiersFormField
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
    class PackageAdminForm(forms.ModelForm):
        best_for = JsonStringListFormField(help_text='Enter one item per line.')
        inclusions = JsonStringListFormField(help_text='Enter one inclusion per line.')
        exclusions = JsonStringListFormField(help_text='Enter one exclusion per line.')
        destination_labels = JsonStringListFormField(help_text='Enter one destination label per line.')
        gallery_urls = JsonStringListFormField(help_text='Enter one image URL per line.')
        tiers = PackageTiersFormField(help_text='One tier per line: name | price | optional note.')

        class Meta:
            model = Package
            fields = '__all__'

    form = PackageAdminForm
    list_display = ['name', 'category', 'duration_days', 'price', 'discount_price', 'is_featured']
    list_filter = ['category', 'destinations', 'is_featured', 'duration_days']
    search_fields = ['name', 'tagline', 'description', 'overview']
    prepopulated_fields = {'slug': ['name']}
    filter_horizontal = ['destinations', 'gallery', 'gallery_assets']
    autocomplete_fields = ['image_media_asset', 'card_media_asset', 'hero_media_asset']
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 'slug', 'tagline', 'description', 'overview', 'category', 'icon',
                'image', 'image_media_asset',
                'card_image_url', 'card_media_asset',
                'hero_image_url', 'hero_media_asset'
            )
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
            'fields': ('destination_labels', 'gallery_assets', 'gallery_urls')
        }),
        ('Featured', {
            'fields': ('is_featured',)
        }),
    )

@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption']
