from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import RestaurantViewSet, CuisineViewSet, restaurant_filters

router = DefaultRouter()
router.register('cuisines', CuisineViewSet, basename='cuisine')
router.register('', RestaurantViewSet, basename='restaurant')

urlpatterns = [
    path('filters/', restaurant_filters, name='restaurant-filters'),
    path('', include(router.urls)),
]
