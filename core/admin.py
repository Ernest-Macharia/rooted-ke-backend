from django.contrib import admin
from .models import ContentBlock, SitePage


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ['key', 'title', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['key', 'title']
    readonly_fields = ['updated_at']


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
            'fields': ('summary', 'body', 'content')
        }),
        ('Metadata', {
            'fields': ('updated_at',)
        }),
    )
