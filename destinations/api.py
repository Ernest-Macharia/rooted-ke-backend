from rest_framework import serializers, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Destination, DestinationImage, DestinationTag


class DestinationImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = DestinationImage
        fields = ['id', 'image', 'is_primary', 'alt_text']

    def get_image(self, obj):
        if obj.image_url:
            return obj.image_url
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class DestinationTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationTag
        fields = ['id', 'name', 'slug']


class DestinationRestaurantLiteSerializer(serializers.Serializer):
    name = serializers.CharField()
    area = serializers.CharField(allow_blank=True)
    cuisine = serializers.CharField(allow_blank=True)
    budget = serializers.CharField(allow_blank=True)
    img = serializers.CharField(allow_blank=True, allow_null=True)


class DestinationSerializer(serializers.ModelSerializer):
    images = DestinationImageSerializer(many=True, read_only=True)
    tags = DestinationTagSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()

    # Frontend-aligned fields
    img = serializers.SerializerMethodField()
    heroImg = serializers.SerializerMethodField()
    packageLink = serializers.CharField(source='package_link', read_only=True)
    things = serializers.ListField(source='things_to_do', read_only=True)
    hotelSearch = serializers.CharField(source='hotel_search', read_only=True)
    restaurants = serializers.SerializerMethodField()
    highlights = serializers.ListField(read_only=True)

    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'short', 'description', 'overview', 'location',
            'latitude', 'longitude', 'price_from', 'rating', 'is_featured',
            'display_tags', 'tags', 'images', 'primary_image',
            'img', 'heroImg', 'highlights', 'packageLink', 'restaurants',
            'things', 'hotelSearch', 'created_at', 'updated_at'
        ]

    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return DestinationImageSerializer(primary, context=self.context).data
        return None

    def get_img(self, obj):
        if obj.card_image_url:
            return obj.card_image_url
        primary = obj.images.filter(is_primary=True).first() or obj.images.first()
        if not primary:
            return None
        if primary.image_url:
            return primary.image_url
        if primary.image:
            request = self.context.get('request')
            return request.build_absolute_uri(primary.image.url) if request else primary.image.url
        return None

    def get_heroImg(self, obj):
        if obj.hero_image_url:
            return obj.hero_image_url
        return self.get_img(obj)

    def get_restaurants(self, obj):
        # Lazy import to avoid circular dependency at import time.
        from restaurants.models import Restaurant

        queryset = (
            Restaurant.objects
            .filter(destination=obj)
            .prefetch_related('cuisine')
            .order_by('-is_featured', '-rating', 'name')[:5]
        )

        data = []
        for restaurant in queryset:
            cuisine_name = restaurant.cuisine.first().name if restaurant.cuisine.exists() else ''
            data.append({
                'name': restaurant.name,
                'area': restaurant.area or obj.location,
                'cuisine': cuisine_name,
                'budget': restaurant.budget_label or restaurant.get_budget_tier_display().split(' ')[0],
                'img': restaurant.image_url,
            })

        return DestinationRestaurantLiteSerializer(data, many=True).data


class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_featured', 'tags__slug']
    search_fields = ['name', 'short', 'description', 'overview', 'location', 'tags__name']
    ordering_fields = ['price_from', 'rating', 'created_at', 'name']
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('images', 'tags')
