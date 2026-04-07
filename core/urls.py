from django.urls import path
from .api import homepage_data, trending_data

urlpatterns = [
    path('homepage/', homepage_data, name='homepage'),
    path('trending/', trending_data, name='trending'),
]