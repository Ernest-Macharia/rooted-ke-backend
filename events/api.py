from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Event, EventBooking


class EventSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    is_upcoming = serializers.SerializerMethodField()

    # Frontend-aligned aliases
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    area = serializers.CharField(read_only=True)
    priceDisplay = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()
    lineup = serializers.ListField(read_only=True)
    ticketLink = serializers.CharField(source='ticket_link', read_only=True)
    whatToPair = serializers.CharField(source='what_to_pair', read_only=True)
    tips = serializers.ListField(read_only=True)
    tags = serializers.ListField(read_only=True)
    gallery = serializers.ListField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'short', 'description', 'category',
            'destination', 'destination_name', 'venue', 'area', 'address',
            'start_date', 'end_date', 'date', 'time',
            'price', 'priceDisplay', 'capacity',
            'image', 'img', 'image_url',
            'lineup', 'ticketLink', 'whatToPair', 'tips', 'tags', 'gallery',
            'is_featured', 'is_upcoming', 'created_at'
        ]

    def get_is_upcoming(self, obj):
        return obj.start_date > timezone.now()

    def get_date(self, obj):
        return obj.start_date.strftime('%B %-d, %Y') if obj.start_date else ''

    def get_time(self, obj):
        if obj.time_display:
            return obj.time_display
        if obj.start_date and obj.end_date:
            return f"{obj.start_date.strftime('%-I:%M%p')} – {obj.end_date.strftime('%-I:%M%p')}"
        return ''

    def get_priceDisplay(self, obj):
        if obj.price_display:
            return obj.price_display
        return str(obj.price) if obj.price is not None else ''

    def get_img(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        if obj.image_url:
            return obj.image_url
        return None


class EventBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = ['id', 'event', 'name', 'email', 'phone', 'tickets', 'booking_date']
        read_only_fields = ['booking_date']


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.select_related('destination').all()
    serializer_class = EventSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'destination__slug', 'is_featured']
    search_fields = ['title', 'short', 'description', 'venue']
    ordering_fields = ['start_date', 'price', 'created_at']
    ordering = ['start_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('upcoming') == 'true':
            queryset = queryset.filter(start_date__gte=timezone.now())
        return queryset


class EventBookingViewSet(viewsets.ModelViewSet):
    queryset = EventBooking.objects.all()
    serializer_class = EventBookingSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']


@api_view(['GET'])
def event_categories(request):
    categories = [
        {'key': 'weekend', 'label': 'This Weekend', 'icon': '📅', 'desc': "What's happening this weekend across Kenya"},
        {'key': 'concerts', 'label': 'Concerts & Festivals', 'icon': '🎵', 'desc': 'Live music, festivals, and cultural celebrations'},
        {'key': 'nightlife', 'label': 'Nightlife & Parties', 'icon': '🎉', 'desc': 'Club nights, themed parties, and social events'},
        {'key': 'cultural', 'label': 'Cultural & Pop-Ups', 'icon': '👥', 'desc': 'Art shows, markets, and community gatherings'},
        {'key': 'sports', 'label': 'Sports & Outdoor', 'icon': '🏃', 'desc': 'Marathons, hikes, and active events'},
    ]
    return Response(categories)
