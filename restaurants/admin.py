from django.contrib import admin
from .models import Restaurant, Cuisine, RestaurantReview

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'destination', 'budget_tier', 'rating', 'is_featured']
    list_filter = ['budget_tier', 'cuisine', 'destination', 'is_featured']
    search_fields = ['name', 'description', 'address']
    prepopulated_fields = {'slug': ['name']}
    filter_horizontal = ['cuisine']

@admin.register(RestaurantReview)
class RestaurantReviewAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']