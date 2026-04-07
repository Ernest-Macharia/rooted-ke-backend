from rest_framework import serializers, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from destinations.models import Destination
from restaurants.models import Restaurant
from events.models import Event
from packages.models import Package
from blog.models import BlogPost
from django.utils import timezone

@api_view(['GET'])
def homepage_data(request):
    """Aggregate data for homepage"""
    # Featured Destinations
    featured_destinations = Destination.objects.filter(is_featured=True)[:6]
    
    # Trending (based on packages or views - customize as needed)
    trending_packages = Package.objects.filter(is_featured=True)[:6]
    
    # Upcoming Events
    upcoming_events = Event.objects.filter(
        start_date__gte=timezone.now(),
        is_featured=True
    )[:6]
    
    # Featured Restaurants
    featured_restaurants = Restaurant.objects.filter(is_featured=True)[:6]
    
    # Latest Blog Posts
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    # Popular Packages
    popular_packages = Package.objects.filter(is_featured=True)[:8]
    
    data = {
        'featured_destinations': DestinationSerializer(featured_destinations, many=True).data,
        'trending_packages': PackageSerializer(trending_packages, many=True).data,
        'upcoming_events': EventSerializer(upcoming_events, many=True).data,
        'featured_restaurants': RestaurantSerializer(featured_restaurants, many=True).data,
        'latest_posts': BlogPostSerializer(latest_posts, many=True).data,
        'popular_packages': PackageSerializer(popular_packages, many=True).data,
    }
    
    return Response(data)

@api_view(['GET'])
def trending_data(request):
    """Get trending destinations and packages"""
    trending_destinations = Destination.objects.filter(is_featured=True)[:6]
    trending_packages = Package.objects.filter(is_featured=True)[:6]
    
    return Response({
        'destinations': DestinationSerializer(trending_destinations, many=True).data,
        'packages': PackageSerializer(trending_packages, many=True).data,
    })

# Import serializers from other apps
from destinations.api import DestinationSerializer
from packages.api import PackageSerializer
from events.api import EventSerializer
from restaurants.api import RestaurantSerializer
from blog.api import BlogPostSerializer