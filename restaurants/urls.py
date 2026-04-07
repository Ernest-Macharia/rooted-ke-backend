from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import RestaurantViewSet

router = DefaultRouter()
router.register('', RestaurantViewSet, basename='restaurant')

urlpatterns = [
    path('', include(router.urls)),
]