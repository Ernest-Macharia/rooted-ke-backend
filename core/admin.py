from pathlib import Path

from django import forms
from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path, reverse
from .models import ContentBlock, SitePage, HomePageSettings, HomePageFeatureItem, MediaAsset


class MediaAssetBulkUploadForm(forms.Form):
    class MultiFileInput(forms.ClearableFileInput):
        allow_multiple_selected = True

    files = forms.FileField(
        label='Images',
        widget=MultiFileInput(),
        help_text='Select multiple image files to upload in one go.',
    )
    default_tags = forms.CharField(
        required=False,
        help_text='Optional comma-separated tags applied to all uploaded files.',
    )
    is_active = forms.BooleanField(required=False, initial=True)


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'alt_text', 'tags', 'image_url']
    readonly_fields = ['created_at', 'updated_at']
    change_list_template = 'admin/core/mediaasset/change_list.html'
    fieldsets = (
        ('Asset', {
            'fields': ('title', 'image', 'image_url', 'alt_text', 'tags', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'bulk-upload/',
                self.admin_site.admin_view(self.bulk_upload_view),
                name='core_mediaasset_bulk_upload',
            ),
        ]
        return custom_urls + urls

    def bulk_upload_view(self, request):
        form = MediaAssetBulkUploadForm(request.POST or None, request.FILES or None)

        if request.method == 'POST' and form.is_valid():
            uploaded_files = request.FILES.getlist('files')
            if not uploaded_files:
                form.add_error('files', 'Please choose at least one file.')
            else:
                created = 0
                default_tags = form.cleaned_data.get('default_tags', '').strip()
                is_active = form.cleaned_data.get('is_active', True)

                for uploaded_file in uploaded_files:
                    title = Path(uploaded_file.name).stem.replace('_', ' ').replace('-', ' ').strip()
                    asset = MediaAsset(
                        title=title or uploaded_file.name,
                        tags=default_tags,
                        is_active=is_active,
                    )
                    asset.image = uploaded_file
                    asset.save()
                    created += 1

                self.message_user(
                    request,
                    f'Successfully uploaded {created} media asset(s).',
                    level=messages.SUCCESS,
                )
                return redirect(reverse('admin:core_mediaasset_changelist'))

        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'title': 'Bulk Upload Media Assets',
            'form': form,
        }
        return render(request, 'admin/core/mediaasset/bulk_upload.html', context)


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
