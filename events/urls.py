from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import EventViewSet, EventBookingViewSet

router = DefaultRouter()
router.register('', EventViewSet, basename='event')
router.register('bookings', EventBookingViewSet, basename='event-booking')

urlpatterns = [
    path('', include(router.urls)),
]