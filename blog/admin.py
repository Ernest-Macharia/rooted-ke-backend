from django.contrib import admin
from django import forms

from core.admin_json_fields import BlogBodyBlocksFormField, JsonStringListFormField
from .models import BlogPost, BlogCategory, BlogComment

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    class BlogPostAdminForm(forms.ModelForm):
        body_blocks = BlogBodyBlocksFormField(
            label='Body blocks',
            help_text='Use one line per block in the format: type | text (types: intro, h2, p, tip).',
        )
        related_slugs = JsonStringListFormField(
            help_text='Enter one related blog slug per line.',
        )

        class Meta:
            model = BlogPost
            fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance and self.instance.pk:
                self.fields['body_blocks'].initial = self.instance.body

        def save(self, commit=True):
            instance = super().save(commit=False)
            instance.body = self.cleaned_data.get('body_blocks', [])
            if commit:
                instance.save()
                self.save_m2m()
            return instance

    form = BlogPostAdminForm
    list_display = ['title', 'author', 'category', 'is_published', 'published_at', 'views']
    list_filter = ['is_published', 'category', 'destination', 'published_at']
    search_fields = ['title', 'excerpt', 'content', 'author']
    prepopulated_fields = {'slug': ['title']}
    autocomplete_fields = ['featured_media_asset', 'author_avatar_media_asset', 'destination']
    date_hierarchy = 'published_at'
    readonly_fields = ['views']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'body_blocks', 'featured_image', 'image_url', 'featured_media_asset')
        }),
        ('Metadata', {
            'fields': (
                'author', 'author_avatar', 'author_avatar_url', 'author_avatar_media_asset',
                'category', 'destination', 'tags', 'related_slugs'
            )
        }),
        ('Frontend Display', {
            'fields': ('date_display', 'read_time')
        }),
        ('Status', {
            'fields': ('is_published', 'views')
        }),
    )

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author', 'content']
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"
