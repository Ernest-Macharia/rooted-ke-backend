from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import BookingEnquiryViewSet

router = DefaultRouter()
router.register('enquiries', BookingEnquiryViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]