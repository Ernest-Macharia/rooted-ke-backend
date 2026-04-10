from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import PackageViewSet, PackageCategoryViewSet

router = DefaultRouter()
router.register('categories', PackageCategoryViewSet, basename='package-category')
router.register('', PackageViewSet, basename='package')

urlpatterns = [
    path('', include(router.urls)),
]
