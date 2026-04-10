from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import BlogPostViewSet, BlogCategoryViewSet, blog_category_labels

router = DefaultRouter()
router.register('categories', BlogCategoryViewSet, basename='blog-category')
router.register('', BlogPostViewSet, basename='blog')

urlpatterns = [
    path('category-labels/', blog_category_labels, name='blog-category-labels'),
    path('', include(router.urls)),
]
