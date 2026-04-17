from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

    # Frontend-aligned aliases
    img = serializers.SerializerMethodField()
    area = serializers.CharField(read_only=True)
    budget = serializers.SerializerMethodField()
    priceRange = serializers.CharField(source='price_range', read_only=True)
    openingHours = serializers.CharField(source='opening_hours', read_only=True)
    bestFor = serializers.ListField(source='best_for', read_only=True)
    mustOrder = serializers.ListField(source='must_order', read_only=True)
    bookingRequired = serializers.BooleanField(source='booking_required', read_only=True)
    location = serializers.CharField(source='location_label', read_only=True)
    tags = serializers.ListField(read_only=True)
    gallery = serializers.ListField(read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'slug', 'short', 'description',
            'destination', 'destination_name',
            'cuisine', 'budget_tier', 'budget_label', 'budget',
            'address', 'area', 'phone', 'email', 'website',
            'opening_hours', 'openingHours',
            'rating', 'image', 'image_url', 'img',
            'price_range', 'priceRange',
            'bestFor', 'mustOrder', 'bookingRequired',
            'location', 'tags', 'gallery',
            'is_featured', 'reviews_count', 'average_rating', 'created_at'
        ]

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else obj.rating

    def get_img(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        if obj.image_url:
            return obj.image_url
        if obj.media_asset:
            if obj.media_asset.image:
                request = self.context.get('request')
                return request.build_absolute_uri(obj.media_asset.image.url) if request else obj.media_asset.image.url
            if obj.media_asset.image_url:
                return obj.media_asset.image_url
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data.get('gallery') and instance.gallery_assets.exists():
            request = self.context.get('request')
            gallery_urls = []
            for asset in instance.gallery_assets.all():
                if asset.image:
                    gallery_urls.append(request.build_absolute_uri(asset.image.url) if request else asset.image.url)
                elif asset.image_url:
                    gallery_urls.append(asset.image_url)
            data['gallery'] = gallery_urls
        return data

    def get_budget(self, obj):
        if obj.budget_label:
            return obj.budget_label
        if obj.budget_tier == 'budget':
            return 'Budget'
        if obj.budget_tier == 'mid':
            return 'Mid'
        if obj.budget_tier == 'luxury':
            return 'Premium'
        return obj.budget_tier


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.prefetch_related('cuisine', 'gallery_assets').select_related('destination', 'media_asset').all()
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['budget_tier', 'destination__slug', 'cuisine__slug', 'is_featured']
    search_fields = ['name', 'short', 'description', 'cuisine__name']
    ordering_fields = ['rating', 'created_at', 'name']
    ordering = ['-rating']


class CuisineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


@api_view(['GET'])
def restaurant_filters(request):
    locations = sorted(set(
        [name for name in Restaurant.objects.values_list('area', flat=True) if name]
        + [name for name in Restaurant.objects.values_list('destination__name', flat=True) if name]
    ))

    cuisines = list(Cuisine.objects.order_by('name').values_list('name', flat=True))

    return Response({
        'locations': locations,
        'budgets': ['Under KES 1,000', 'KES 1,000–3,000', 'KES 3,000+'],
        'cuisines': cuisines,
    })
