from rest_framework import serializers, viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import BookingEnquiry

class BookingEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingEnquiry
        fields = ['id', 'name', 'email', 'phone', 'package', 'destination',
                 'travel_date', 'travelers', 'special_requests', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

class BookingEnquiryViewSet(viewsets.ModelViewSet):
    queryset = BookingEnquiry.objects.all()
    serializer_class = BookingEnquirySerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['created_at', 'travel_date']
    ordering = ['-created_at']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Send email notification (optional)
        try:
            send_mail(
                subject=f"New Booking Enquiry from {serializer.instance.name}",
                message=f"Booking enquiry received for {serializer.instance.package or serializer.instance.destination}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except:
            pass
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
