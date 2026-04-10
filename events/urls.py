from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import EventViewSet, EventBookingViewSet, event_categories

router = DefaultRouter()
router.register('bookings', EventBookingViewSet, basename='event-booking')
router.register('', EventViewSet, basename='event')

urlpatterns = [
    path('categories/', event_categories, name='event-categories'),
    path('', include(router.urls)),
]
