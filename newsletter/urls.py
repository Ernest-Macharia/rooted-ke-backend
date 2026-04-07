from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import SubscriberViewSet

router = DefaultRouter()
router.register('subscribers', SubscriberViewSet, basename='subscriber')

urlpatterns = [
    path('', include(router.urls)),
]