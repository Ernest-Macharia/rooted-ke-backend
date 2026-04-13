from django.contrib import admin
from .models import ContentBlock, SitePage, HomePageSettings, HomePageFeatureItem


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ['key', 'title', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['key', 'title']
    readonly_fields = ['updated_at']
    exclude = ['content']


@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'is_published', 'updated_at']
    list_filter = ['is_published']
    search_fields = ['slug', 'title', 'summary', 'body']
    readonly_fields = ['updated_at']
    fieldsets = (
        ('Page Identity', {
            'fields': ('slug', 'title', 'is_published')
        }),
        ('Content', {
            'fields': ('summary', 'body')
        }),
        ('Section 1', {
            'fields': ('section_1_heading', 'section_1_body')
        }),
        ('Section 2', {
            'fields': ('section_2_heading', 'section_2_body')
        }),
        ('Section 3', {
            'fields': ('section_3_heading', 'section_3_body')
        }),
        ('Metadata', {
            'fields': ('updated_at',)
        }),
    )
    exclude = ['content']


@admin.register(HomePageSettings)
class HomePageSettingsAdmin(admin.ModelAdmin):
    list_display = ['singleton_key', 'is_active', 'updated_at']
    readonly_fields = ['updated_at']
    fieldsets = (
        ('Status', {
            'fields': ('singleton_key', 'is_active')
        }),
        ('Hero Section', {
            'fields': ('hero_eyebrow', 'hero_title', 'hero_subtitle', 'hero_description', 'hero_background_image', 'hero_background_image_url')
        }),
        ('Destinations Section', {
            'fields': ('destinations_eyebrow', 'destinations_title', 'destinations_subtitle', 'destinations_fallback_card_image', 'destinations_fallback_card_image_url')
        }),
        ('Top Categories Section', {
            'fields': ('top_categories_eyebrow', 'top_categories_title')
        }),
        ('Trending Section', {
            'fields': ('trending_eyebrow', 'trending_title', 'trending_subtitle')
        }),
        ('Restaurants Section', {
            'fields': ('restaurants_eyebrow', 'restaurants_title', 'restaurants_subtitle')
        }),
        ('Events Section', {
            'fields': ('events_eyebrow', 'events_title', 'events_subtitle')
        }),
        ('Packages Section', {
            'fields': ('packages_eyebrow', 'packages_title', 'packages_title_emphasis', 'packages_subtitle')
        }),
        ('Blog Section', {
            'fields': ('blog_eyebrow', 'blog_title', 'blog_subtitle', 'blog_cta_label')
        }),
        ('Newsletter Section', {
            'fields': (
                'newsletter_eyebrow',
                'newsletter_title',
                'newsletter_subtitle',
                'newsletter_description',
                'newsletter_disclaimer',
                'newsletter_button_label',
                'newsletter_success_message',
            )
        }),
        ('Metadata', {
            'fields': ('updated_at',)
        }),
    )


@admin.register(HomePageFeatureItem)
class HomePageFeatureItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'homepage_settings', 'sort_order', 'is_active']
    list_filter = ['section', 'is_active']
    search_fields = ['title', 'subtitle', 'cta_label']
    list_editable = ['sort_order', 'is_active']
    fieldsets = (
        ('Placement', {
            'fields': ('homepage_settings', 'section', 'sort_order', 'is_active')
        }),
        ('Content', {
            'fields': ('title', 'subtitle', 'cta_label')
        }),
        ('Image (Upload Or URL)', {
            'fields': ('image', 'image_url')
        }),
    )
