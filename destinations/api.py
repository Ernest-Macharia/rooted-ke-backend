from rest_framework import serializers, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Destination, DestinationImage, DestinationTag

class DestinationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationImage
        fields = ['id', 'image', 'is_primary', 'alt_text']

class DestinationTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationTag
        fields = ['id', 'name', 'slug']

class DestinationSerializer(serializers.ModelSerializer):
    images = DestinationImageSerializer(many=True, read_only=True)
    tags = DestinationTagSerializer(many=True, read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Destination
        fields = ['id', 'name', 'slug', 'description', 'location', 'latitude', 
                 'longitude', 'price_from', 'rating', 'is_featured', 'images', 
                 'tags', 'primary_image', 'created_at', 'updated_at']
    
    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return DestinationImageSerializer(primary).data
        return None

class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_featured', 'tags__slug']
    search_fields = ['name', 'description', 'location', 'tags__name']
    ordering_fields = ['price_from', 'rating', 'created_at', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Prefetch related fields for efficiency
        return queryset.prefetch_related('images', 'tags')