from django.utils import timezone
from rest_framework import serializers, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

from destinations.models import Destination
from restaurants.models import Restaurant
from events.models import Event
from packages.models import Package
from blog.models import BlogPost
from .models import ContentBlock, SitePage


class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = ['id', 'key', 'title', 'content', 'is_active', 'updated_at']


class ContentBlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentBlock.objects.filter(is_active=True)
    serializer_class = ContentBlockSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['key', 'title']
    ordering_fields = ['key', 'updated_at']
    ordering = ['key']
    lookup_field = 'key'


class SitePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitePage
        fields = ['id', 'slug', 'title', 'summary', 'body', 'content', 'is_published', 'updated_at']


class SitePageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SitePage.objects.filter(is_published=True)
    serializer_class = SitePageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['slug', 'title', 'summary', 'body']
    ordering_fields = ['slug', 'updated_at']
    ordering = ['slug']
    lookup_field = 'slug'


@api_view(['GET'])
def homepage_data(request):
    """Aggregate data for homepage plus CMS overrides."""
    featured_destinations = Destination.objects.filter(is_featured=True)[:6]
    trending_packages = Package.objects.filter(is_featured=True)[:6]
    upcoming_events = Event.objects.filter(start_date__gte=timezone.now(), is_featured=True)[:6]
    featured_restaurants = Restaurant.objects.filter(is_featured=True)[:6]
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    popular_packages = Package.objects.filter(is_featured=True)[:8]

    homepage_block = ContentBlock.objects.filter(key='homepage', is_active=True).first()
    nav_block = ContentBlock.objects.filter(key='navigation', is_active=True).first()
    footer_block = ContentBlock.objects.filter(key='footer', is_active=True).first()

    data = {
        'cms': {
            'homepage': homepage_block.content if homepage_block else {},
            'navigation': nav_block.content if nav_block else {},
            'footer': footer_block.content if footer_block else {},
        },
        'featured_destinations': DestinationSerializer(featured_destinations, many=True, context={'request': request}).data,
        'trending_packages': PackageSerializer(trending_packages, many=True, context={'request': request}).data,
        'upcoming_events': EventSerializer(upcoming_events, many=True, context={'request': request}).data,
        'featured_restaurants': RestaurantSerializer(featured_restaurants, many=True, context={'request': request}).data,
        'latest_posts': BlogPostSerializer(latest_posts, many=True, context={'request': request}).data,
        'popular_packages': PackageSerializer(popular_packages, many=True, context={'request': request}).data,
    }

    return Response(data)


@api_view(['GET'])
def trending_data(request):
    trending_destinations = Destination.objects.filter(is_featured=True)[:6]
    trending_packages = Package.objects.filter(is_featured=True)[:6]

    return Response({
        'destinations': DestinationSerializer(trending_destinations, many=True, context={'request': request}).data,
        'packages': PackageSerializer(trending_packages, many=True, context={'request': request}).data,
    })


@api_view(['GET'])
def frontend_bootstrap(request):
    """Single endpoint to fetch constants-like frontend payloads from backend."""
    blocks = ContentBlock.objects.filter(is_active=True)
    pages = SitePage.objects.filter(is_published=True)
    return Response({
        'content_blocks': {item.key: item.content for item in blocks},
        'site_pages': {
            page.slug: {
                'title': page.title,
                'summary': page.summary,
                'body': page.body,
                'content': page.content,
                'updated_at': page.updated_at,
            }
            for page in pages
        }
    })


@api_view(['GET'])
def legal_pages(request):
    legal_slugs = ['privacy-policy', 'terms-of-service']
    pages = SitePage.objects.filter(is_published=True, slug__in=legal_slugs)
    return Response({
        page.slug: {
            'title': page.title,
            'summary': page.summary,
            'body': page.body,
            'content': page.content,
            'updated_at': page.updated_at,
        }
        for page in pages
    })


# Import serializers from other apps
from destinations.api import DestinationSerializer
from packages.api import PackageSerializer
from events.api import EventSerializer
from restaurants.api import RestaurantSerializer
from blog.api import BlogPostSerializer
