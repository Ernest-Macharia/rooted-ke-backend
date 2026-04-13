from django.db import models
from django.utils.text import slugify
from destinations.models import Destination

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField()
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/')
    image_url = models.URLField(blank=True)
    author = models.CharField(max_length=100)
    author_avatar = models.ImageField(upload_to='blog/authors/', null=True, blank=True)
    author_avatar_url = models.URLField(blank=True)
    date_display = models.CharField(max_length=80, blank=True)
    read_time = models.CharField(max_length=40, blank=True)
    category = models.ForeignKey(BlogCategory, related_name='posts', on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")
    body = models.JSONField(default=list, blank=True)
    related_slugs = models.JSONField(default=list, blank=True)
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []

class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"
