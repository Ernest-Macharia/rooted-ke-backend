from rest_framework import serializers, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Event, EventBooking

class EventSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    is_upcoming = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'slug', 'description', 'category', 'destination',
                 'destination_name', 'venue', 'address', 'start_date', 'end_date',
                 'price', 'capacity', 'image', 'is_featured', 'is_upcoming', 'created_at']
    
    def get_is_upcoming(self, obj):
        return obj.start_date > timezone.now()

class EventBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = ['id', 'event', 'name', 'email', 'phone', 'tickets', 'booking_date']
        read_only_fields = ['booking_date']

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'destination__slug', 'is_featured']
    search_fields = ['title', 'description', 'venue']
    ordering_fields = ['start_date', 'price', 'created_at']
    ordering = ['start_date']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter upcoming events if param is passed
        if self.request.query_params.get('upcoming') == 'true':
            queryset = queryset.filter(start_date__gte=timezone.now())
        return queryset


class EventBookingViewSet(viewsets.ModelViewSet):
    queryset = EventBooking.objects.all()
    serializer_class = EventBookingSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
