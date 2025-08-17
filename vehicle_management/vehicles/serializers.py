from rest_framework import serializers
from .models import Vehicle, VehicleImage, Wishlist, Gallery
from django.contrib.auth import get_user_model

User = get_user_model()

class VehicleImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = VehicleImage
        fields = ['id', 'image', 'image_url', 'is_primary', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
    
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    is_wishlisted = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'title', 'year', 'price', 'fuel_type', 'transmission',
            'mileage', 'body_type', 'color', 'engine', 'description',
            'features', 'images', 'uploaded_images', 'is_wishlisted',
            'created_by', 'created_by_username', 'created_at', 'updated_at',
            'is_active'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'is_active']
    
    def get_is_wishlisted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Wishlist.objects.filter(user=request.user, vehicle=obj).exists()
        return False
    
    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        
        # Ensure is_active is always True for new vehicles
        validated_data['is_active'] = True
        
        vehicle = Vehicle.objects.create(**validated_data)
        
        # Handle image uploads
        for i, image in enumerate(uploaded_images):
            VehicleImage.objects.create(
                vehicle=vehicle,
                image=image,
                is_primary=(i == 0)  # First image is primary
            )
        
        return vehicle
    
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        
        # Update vehicle fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Handle new image uploads
        for i, image in enumerate(uploaded_images):
            existing_images_count = instance.images.count()
            VehicleImage.objects.create(
                vehicle=instance,
                image=image,
                is_primary=(existing_images_count == 0 and i == 0)
            )
        
        return instance

class VehicleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing vehicles"""
    primary_image = serializers.SerializerMethodField()
    is_wishlisted = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'title', 'year', 'price', 'fuel_type', 'transmission',
            'mileage', 'body_type', 'color', 'primary_image', 'is_wishlisted',
            'created_by_username', 'created_at'
        ]
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image.url
        elif obj.images.exists():
            return obj.images.first().image.url
        return None
    
    def get_is_wishlisted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Wishlist.objects.filter(user=request.user, vehicle=obj).exists()
        return False

class WishlistSerializer(serializers.ModelSerializer):
    vehicle = VehicleListSerializer(read_only=True)
    vehicle_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'vehicle', 'vehicle_id', 'added_at']
        read_only_fields = ['id', 'added_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

class GallerySerializer(serializers.ModelSerializer):
    """Serializer for standalone gallery images (not attached to vehicles)"""
    image_url = serializers.SerializerMethodField()
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = Gallery
        fields = ['id', 'title', 'description', 'image', 'image_url', 'uploaded_by', 'uploaded_by_username', 'uploaded_at', 'is_active']
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'is_active']
    
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['uploaded_by'] = request.user
        validated_data['is_active'] = True
        return super().create(validated_data) 