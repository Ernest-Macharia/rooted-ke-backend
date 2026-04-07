from rest_framework import serializers, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Package, PackageCategory, PackageImage

class PackageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageCategory
        fields = ['id', 'name', 'slug']

class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageImage
        fields = ['id', 'image', 'caption']

class PackageSerializer(serializers.ModelSerializer):
    category_detail = PackageCategorySerializer(source='category', read_only=True)
    destinations_list = serializers.StringRelatedField(many=True, read_only=True)
    gallery_images = PackageImageSerializer(source='gallery', many=True, read_only=True)
    includes_list = serializers.SerializerMethodField()
    excludes_list = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Package
        fields = ['id', 'name', 'slug', 'description', 'category', 'category_detail',
                 'destinations', 'destinations_list', 'duration_days', 'duration_nights',
                 'price', 'discount_price', 'final_price', 'includes', 'includes_list',
                 'excludes', 'excludes_list', 'itinerary', 'image', 'gallery_images',
                 'is_featured', 'created_at']
    
    def get_includes_list(self, obj):
        return [item.strip() for item in obj.includes.split(',')] if obj.includes else []
    
    def get_excludes_list(self, obj):
        return [item.strip() for item in obj.excludes.split(',')] if obj.excludes else []
    
    def get_final_price(self, obj):
        return obj.discount_price if obj.discount_price else obj.price

class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'destinations__slug', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'duration_days', 'created_at']
    ordering = ['-created_at']
