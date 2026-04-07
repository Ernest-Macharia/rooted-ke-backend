from django.db import models
from rest_framework import serializers, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Restaurant, Cuisine, RestaurantReview

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['id', 'name', 'slug']

class RestaurantReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantReview
        fields = ['id', 'author', 'rating', 'comment', 'created_at']

class RestaurantSerializer(serializers.ModelSerializer):
    cuisine = CuisineSerializer(many=True, read_only=True)
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'slug', 'description', 'destination', 'destination_name',
                 'cuisine', 'budget_tier', 'address', 'phone', 'email', 'website',
                 'opening_hours', 'rating', 'image', 'is_featured', 'reviews_count',
                 'average_rating', 'created_at']
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()
    
    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else obj.rating

class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['budget_tier', 'destination__slug', 'cuisine__slug', 'is_featured']
    search_fields = ['name', 'description', 'cuisine__name']
    ordering_fields = ['rating', 'created_at', 'name']
    ordering = ['-rating']
