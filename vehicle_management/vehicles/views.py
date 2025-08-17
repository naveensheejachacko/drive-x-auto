from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Vehicle, VehicleImage, Wishlist
from .serializers import (
    VehicleSerializer, VehicleListSerializer, VehicleImageSerializer,
    WishlistSerializer, GalleryImageSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly
import random

class VehicleListCreateView(generics.ListCreateAPIView):
    """
    List all vehicles or create a new vehicle (admin only)
    """
    queryset = Vehicle.objects.filter(is_active=True)
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return VehicleListSerializer
        return VehicleSerializer
    
    def get_queryset(self):
        queryset = Vehicle.objects.filter(is_active=True)
        
        # Add search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(color__icontains=search) |
                Q(fuel_type__icontains=search) |
                Q(body_type__icontains=search)
            )
        
        # Add filtering
        fuel_type = self.request.query_params.get('fuel_type', None)
        if fuel_type:
            queryset = queryset.filter(fuel_type=fuel_type)
        
        body_type = self.request.query_params.get('body_type', None)
        if body_type:
            queryset = queryset.filter(body_type=body_type)
        
        transmission = self.request.query_params.get('transmission', None)
        if transmission:
            queryset = queryset.filter(transmission=transmission)
        
        # Price range filtering
        min_price = self.request.query_params.get('min_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        max_price = self.request.query_params.get('max_price', None)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Year range filtering
        min_year = self.request.query_params.get('min_year', None)
        if min_year:
            queryset = queryset.filter(year__gte=min_year)
        
        max_year = self.request.query_params.get('max_year', None)
        if max_year:
            queryset = queryset.filter(year__lte=max_year)
        
        return queryset.order_by('-created_at')

class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a vehicle (update/delete: owner or admin only)
    """
    queryset = Vehicle.objects.filter(is_active=True)
    serializer_class = VehicleSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    
    def destroy(self, request, *args, **kwargs):
        # Soft delete
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'message': 'Vehicle deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class GalleryView(generics.ListAPIView):
    """
    Gallery view showing random vehicle images for feed
    """
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get random vehicle images
        images = list(VehicleImage.objects.filter(vehicle__is_active=True))
        random.shuffle(images)
        
        # Limit to 50 random images for performance
        limit = int(self.request.query_params.get('limit', 50))
        return images[:limit]

class WishlistView(generics.ListCreateAPIView):
    """
    List user's wishlist or add vehicle to wishlist
    """
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_from_wishlist(request, vehicle_id):
    """
    Remove vehicle from user's wishlist
    """
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, vehicle_id=vehicle_id)
        wishlist_item.delete()
        return Response({'message': 'Vehicle removed from wishlist'}, status=status.HTTP_204_NO_CONTENT)
    except Wishlist.DoesNotExist:
        return Response({'error': 'Vehicle not in wishlist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_wishlist(request, vehicle_id):
    """
    Toggle vehicle in user's wishlist
    """
    try:
        vehicle = get_object_or_404(Vehicle, id=vehicle_id, is_active=True)
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            vehicle=vehicle
        )
        
        if created:
            return Response({
                'message': 'Vehicle added to wishlist',
                'is_wishlisted': True
            }, status=status.HTTP_201_CREATED)
        else:
            wishlist_item.delete()
            return Response({
                'message': 'Vehicle removed from wishlist',
                'is_wishlisted': False
            }, status=status.HTTP_200_OK)
    
    except Vehicle.DoesNotExist:
        return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)

class VehicleImageView(generics.ListCreateAPIView):
    """
    List or add images for a specific vehicle
    """
    serializer_class = VehicleImageSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    
    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        return VehicleImage.objects.filter(vehicle_id=vehicle_id)
    
    def perform_create(self, serializer):
        vehicle_id = self.kwargs['vehicle_id']
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        
        # Check if user has permission to add images to this vehicle
        if vehicle.created_by != self.request.user and not self.request.user.is_admin:
            raise permissions.PermissionDenied("You don't have permission to add images to this vehicle.")
        
        serializer.save(vehicle=vehicle)

@api_view(['DELETE'])
@permission_classes([IsOwnerOrAdminOrReadOnly])
def delete_vehicle_image(request, vehicle_id, image_id):
    """
    Delete a specific vehicle image
    """
    try:
        image = VehicleImage.objects.get(id=image_id, vehicle_id=vehicle_id)
        vehicle = image.vehicle
        
        # Check permissions
        if vehicle.created_by != request.user and not request.user.is_admin:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        image.delete()
        return Response({'message': 'Image deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    except VehicleImage.DoesNotExist:
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def vehicle_stats(request):
    """
    Get vehicle statistics (admin only)
    """
    if not request.user.is_admin:
        return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    
    total_vehicles = Vehicle.objects.filter(is_active=True).count()
    total_wishlists = Wishlist.objects.count()
    total_images = VehicleImage.objects.count()
    
    return Response({
        'total_vehicles': total_vehicles,
        'total_wishlists': total_wishlists,
        'total_images': total_images,
    })
