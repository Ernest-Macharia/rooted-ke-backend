from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import (
    homepage_data,
    trending_data,
    frontend_bootstrap,
    legal_pages,
    page_detail,
    about_page,
    privacy_policy_page,
    terms_of_service_page,
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
    path('pages/about/', about_page, name='about-page'),
    path('pages/privacy-policy/', privacy_policy_page, name='privacy-policy-page'),
    path('pages/terms-of-service/', terms_of_service_page, name='terms-of-service-page'),
    path('pages/<slug:slug>/', page_detail, name='page-detail'),
    path('', include(router.urls)),
]
