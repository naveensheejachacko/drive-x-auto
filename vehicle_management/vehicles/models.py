from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
import json

User = get_user_model()

class Vehicle(models.Model):
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('hybrid_electric', 'Hybrid Electric'),
        ('gas', 'Gas'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('cvt', 'CVT'),
    ]
    
    BODY_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('saloon', 'Saloon'),
        ('hatchback', 'Hatchback'),
        ('suv', 'SUV'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('wagon', 'Wagon'),
        ('pickup', 'Pickup'),
        ('van', 'Van'),
    ]
    
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    transmission = models.CharField(max_length=15, choices=TRANSMISSION_CHOICES)
    mileage = models.CharField(max_length=50)  # e.g., "60,000 miles"
    body_type = models.CharField(max_length=15, choices=BODY_TYPE_CHOICES)
    color = models.CharField(max_length=50)
    engine = models.CharField(max_length=100)
    description = models.TextField()
    features = models.JSONField(default=list)  # Array of features
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} ({self.year})"

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'uploaded_at']
        
    def __str__(self):
        return f"Image for {self.vehicle.title}"
    
    def save(self, *args, **kwargs):
        # Ensure only one primary image per vehicle
        if self.is_primary:
            VehicleImage.objects.filter(vehicle=self.vehicle, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)



class Gallery(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = CloudinaryField('image')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gallery_images')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
        
    def __str__(self):
        return f"Gallery Image: {self.title or 'Untitled'} - {self.uploaded_at.strftime('%Y-%m-%d')}"
