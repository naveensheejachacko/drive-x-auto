from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    # Vehicle CRUD operations
    path('', views.VehicleListCreateView.as_view(), name='vehicle-list-create'),
    path('<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle-detail'),
    
    # Gallery (standalone images, not attached to vehicles)
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('gallery/<int:pk>/', views.GalleryDetailView.as_view(), name='gallery-detail'),
    
    # Wishlist operations
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('<int:vehicle_id>/wishlist/toggle/', views.toggle_wishlist, name='toggle-wishlist'),
    path('<int:vehicle_id>/wishlist/remove/', views.remove_from_wishlist, name='remove-wishlist'),
    
    # Vehicle images
    path('<int:vehicle_id>/images/', views.VehicleImageView.as_view(), name='vehicle-images'),
    path('<int:vehicle_id>/images/<int:image_id>/delete/', views.delete_vehicle_image, name='delete-vehicle-image'),
    
    # Statistics (admin only)
    path('stats/', views.vehicle_stats, name='vehicle-stats'),
] 