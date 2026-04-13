from django.utils import timezone
from rest_framework import serializers, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

from destinations.models import Destination
from restaurants.models import Restaurant
from events.models import Event
from packages.models import Package
from blog.models import BlogPost
from .models import ContentBlock, SitePage, HomePageSettings, HomePageFeatureItem


def _page_payload(page):
    return {
        'title': page.title,
        'summary': page.summary,
        'body': page.body,
        'section_1_heading': page.section_1_heading,
        'section_1_body': page.section_1_body,
        'section_2_heading': page.section_2_heading,
        'section_2_body': page.section_2_body,
        'section_3_heading': page.section_3_heading,
        'section_3_body': page.section_3_body,
        'updated_at': page.updated_at,
    }


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
        fields = [
            'id', 'slug', 'title', 'summary', 'body',
            'section_1_heading', 'section_1_body',
            'section_2_heading', 'section_2_body',
            'section_3_heading', 'section_3_body',
            'is_published', 'updated_at',
        ]


class HomePageSettingsSerializer(serializers.ModelSerializer):
    hero_background_image_src = serializers.SerializerMethodField()
    destinations_fallback_card_image_src = serializers.SerializerMethodField()
    top_primary_items = serializers.SerializerMethodField()
    top_secondary_items = serializers.SerializerMethodField()
    trending_items = serializers.SerializerMethodField()

    class Meta:
        model = HomePageSettings
        fields = [
            'hero_eyebrow',
            'hero_title',
            'hero_subtitle',
            'hero_description',
            'hero_background_image_src',
            'hero_background_image_url',
            'destinations_eyebrow',
            'destinations_title',
            'destinations_subtitle',
            'destinations_fallback_card_image_src',
            'destinations_fallback_card_image_url',
            'top_categories_eyebrow',
            'top_categories_title',
            'trending_eyebrow',
            'trending_title',
            'trending_subtitle',
            'restaurants_eyebrow',
            'restaurants_title',
            'restaurants_subtitle',
            'events_eyebrow',
            'events_title',
            'events_subtitle',
            'packages_eyebrow',
            'packages_title',
            'packages_title_emphasis',
            'packages_subtitle',
            'blog_eyebrow',
            'blog_title',
            'blog_subtitle',
            'blog_cta_label',
            'newsletter_eyebrow',
            'newsletter_title',
            'newsletter_subtitle',
            'newsletter_description',
            'newsletter_disclaimer',
            'newsletter_button_label',
            'newsletter_success_message',
            'top_primary_items',
            'top_secondary_items',
            'trending_items',
            'updated_at',
        ]

    def _absolute_media_url(self, file_field):
        if not file_field:
            return ''
        request = self.context.get('request')
        return request.build_absolute_uri(file_field.url) if request else file_field.url

    def get_hero_background_image_src(self, obj):
        return self._absolute_media_url(obj.hero_background_image)

    def get_destinations_fallback_card_image_src(self, obj):
        return self._absolute_media_url(obj.destinations_fallback_card_image)

    def _serialize_items(self, obj, section):
        queryset = obj.feature_items.filter(section=section, is_active=True).order_by('sort_order', 'id')
        return HomePageFeatureItemSerializer(queryset, many=True, context=self.context).data

    def get_top_primary_items(self, obj):
        return self._serialize_items(obj, 'top_primary')

    def get_top_secondary_items(self, obj):
        return self._serialize_items(obj, 'top_secondary')

    def get_trending_items(self, obj):
        return self._serialize_items(obj, 'trending')


class HomePageFeatureItemSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = HomePageFeatureItem
        fields = ['title', 'subtitle', 'cta_label', 'img', 'image_url', 'sort_order']

    def get_img(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return obj.image_url


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

    homepage_settings = HomePageSettings.objects.filter(is_active=True).first()
    homepage_block = ContentBlock.objects.filter(key='homepage', is_active=True).first()
    nav_block = ContentBlock.objects.filter(key='navigation', is_active=True).first()
    footer_block = ContentBlock.objects.filter(key='footer', is_active=True).first()

    data = {
        'cms': {
            'homepage': (
                HomePageSettingsSerializer(homepage_settings, context={'request': request}).data
                if homepage_settings
                else (homepage_block.content if homepage_block else {})
            ),
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
            page.slug: _page_payload(page)
            for page in pages
        }
    })


@api_view(['GET'])
def legal_pages(request):
    legal_slugs = ['privacy-policy', 'terms-of-service']
    pages = SitePage.objects.filter(is_published=True, slug__in=legal_slugs)
    return Response({
        page.slug: _page_payload(page)
        for page in pages
    })


@api_view(['GET'])
def page_detail(request, slug):
    page = SitePage.objects.filter(is_published=True, slug=slug).first()
    if not page:
        return Response({'detail': 'Not found.'}, status=404)
    return Response(SitePageSerializer(page, context={'request': request}).data)


@api_view(['GET'])
def about_page(request):
    page = SitePage.objects.filter(is_published=True, slug='about').first()
    if not page:
        return Response({'detail': 'Not found.'}, status=404)
    return Response(SitePageSerializer(page, context={'request': request}).data)


@api_view(['GET'])
def privacy_policy_page(request):
    page = SitePage.objects.filter(is_published=True, slug='privacy-policy').first()
    if not page:
        return Response({'detail': 'Not found.'}, status=404)
    return Response(SitePageSerializer(page, context={'request': request}).data)


@api_view(['GET'])
def terms_of_service_page(request):
    page = SitePage.objects.filter(is_published=True, slug='terms-of-service').first()
    if not page:
        return Response({'detail': 'Not found.'}, status=404)
    return Response(SitePageSerializer(page, context={'request': request}).data)


# Import serializers from other apps
from destinations.api import DestinationSerializer
from packages.api import PackageSerializer
from events.api import EventSerializer
from restaurants.api import RestaurantSerializer
from blog.api import BlogPostSerializer
