"""URL configuration for records application"""
from django.urls import path, include

urlpatterns = [
    path('', include('apps.records.api.urls')),
]
