from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import (
    homepage_data,
    trending_data,
    frontend_bootstrap,
    legal_pages,
    ContentBlockViewSet,
    SitePageViewSet,
)

router = DefaultRouter()
router.register('content-blocks', ContentBlockViewSet, basename='content-block')
router.register('site-pages', SitePageViewSet, basename='site-page')

urlpatterns = [
    path('homepage/', homepage_data, name='homepage'),
    path('trending/', trending_data, name='trending'),
    path('frontend-bootstrap/', frontend_bootstrap, name='frontend-bootstrap'),
    path('legal-pages/', legal_pages, name='legal-pages'),
    path('', include(router.urls)),
]
