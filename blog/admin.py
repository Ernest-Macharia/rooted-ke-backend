from django.contrib import admin
from .models import BlogPost, BlogCategory, BlogComment

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'published_at', 'views']
    list_filter = ['is_published', 'category', 'destination', 'published_at']
    search_fields = ['title', 'excerpt', 'content', 'author']
    prepopulated_fields = {'slug': ['title']}
    date_hierarchy = 'published_at'
    readonly_fields = ['views']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'body', 'featured_image', 'image_url')
        }),
        ('Metadata', {
            'fields': ('author', 'author_avatar_url', 'category', 'destination', 'tags', 'related_slugs')
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
