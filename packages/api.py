from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets, filters

from .models import Package, PackageCategory, PackageImage


class PackageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageCategory
        fields = ['id', 'name', 'slug']


class PackageImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PackageImage
        fields = ['id', 'image', 'caption']

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class PackageSerializer(serializers.ModelSerializer):
    category_detail = PackageCategorySerializer(source='category', read_only=True)
    destinations_list = serializers.StringRelatedField(many=True, read_only=True)
    gallery_images = PackageImageSerializer(source='gallery', many=True, read_only=True)

    includes_list = serializers.SerializerMethodField()
    excludes_list = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    # Frontend-aligned aliases
    title = serializers.CharField(source='name', read_only=True)
    sub = serializers.CharField(source='description', read_only=True)
    key = serializers.CharField(source='slug', read_only=True)
    img = serializers.SerializerMethodField()
    heroImg = serializers.SerializerMethodField()
    duration = serializers.CharField(read_only=True)
    categoryLabel = serializers.SerializerMethodField()
    bestFor = serializers.ListField(source='best_for', read_only=True)
    inclusions = serializers.ListField(read_only=True)
    exclusions = serializers.ListField(read_only=True)
    tiers = serializers.ListField(read_only=True)
    destinations = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = [
            'id', 'name', 'title', 'slug', 'key', 'tagline',
            'description', 'sub', 'overview',
            'category', 'category_detail', 'categoryLabel',
            'duration_days', 'duration_nights', 'duration',
            'price', 'discount_price', 'final_price',
            'includes', 'includes_list', 'excludes', 'excludes_list',
            'itinerary',
            'image', 'card_image_url', 'hero_image_url', 'img', 'heroImg',
            'icon', 'bestFor', 'inclusions', 'exclusions', 'tiers',
            'destinations', 'destinations_list', 'destination_labels',
            'gallery', 'gallery_urls', 'gallery_images',
            'is_featured', 'created_at', 'updated_at'
        ]

    def get_includes_list(self, obj):
        return [item.strip() for item in obj.includes.split(',')] if obj.includes else []

    def get_excludes_list(self, obj):
        return [item.strip() for item in obj.excludes.split(',')] if obj.excludes else []

    def get_final_price(self, obj):
        return obj.discount_price if obj.discount_price else obj.price

    def get_img(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        if obj.card_image_url:
            return obj.card_image_url
        return None

    def get_heroImg(self, obj):
        if obj.hero_image_url:
            return obj.hero_image_url
        return self.get_img(obj)

    def get_categoryLabel(self, obj):
        return obj.category.name if obj.category else ''

    def get_destinations(self, obj):
        if obj.destination_labels:
            return obj.destination_labels
        return [item.name for item in obj.destinations.all()]

    def get_gallery(self, obj):
        if obj.gallery_urls:
            return obj.gallery_urls
        images = []
        request = self.context.get('request')
        for item in obj.gallery.all():
            if item.image:
                images.append(request.build_absolute_uri(item.image.url) if request else item.image.url)
        return images


class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.prefetch_related('destinations', 'gallery').select_related('category').all()
    serializer_class = PackageSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'destinations__slug', 'is_featured']
    search_fields = ['name', 'tagline', 'description', 'overview']
    ordering_fields = ['price', 'duration_days', 'created_at']
    ordering = ['name']


class PackageCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PackageCategory.objects.all()
    serializer_class = PackageCategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'slug']
    ordering_fields = ['name']
    ordering = ['name']
