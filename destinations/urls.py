from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import DestinationViewSet

router = DefaultRouter()
router.register('', DestinationViewSet, basename='destination')

urlpatterns = [
    path('', include(router.urls)),
]