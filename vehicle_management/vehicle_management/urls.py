"""
URL configuration for vehicle_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_root(request):
    """
    API Root - provides overview of available endpoints
    """
    return Response({
        'message': 'Vehicle Management API',
        'version': 'v1',
        'endpoints': {
            'authentication': {
                'register': '/api/v1/auth/register/',
                'login': '/api/v1/auth/login/',
                'logout': '/api/v1/auth/logout/',
                'profile': '/api/v1/auth/profile/',
            },
            'vehicles': {
                'list_create': '/api/v1/vehicles/',
                'detail': '/api/v1/vehicles/{id}/',
                'wishlist': '/api/v1/vehicles/wishlist/',
                'toggle_wishlist': '/api/v1/vehicles/{id}/wishlist/toggle/',
                'stats': '/api/v1/vehicles/stats/',
            },
            'gallery': {
                'list_create': '/api/v1/vehicles/gallery/',
                'detail': '/api/v1/vehicles/gallery/{id}/',
                'description': 'Standalone gallery images (not attached to vehicles)',
            }
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api_root, name='api-root'),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/vehicles/', include('vehicles.urls')),
]
