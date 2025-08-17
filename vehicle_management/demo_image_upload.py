#!/usr/bin/env python
"""
Demo script showing how to create a vehicle with images in a single request.
This demonstrates the multipart/form-data approach.
"""

import requests
import os
from io import BytesIO
from PIL import Image

# Configuration
BASE_URL = "http://localhost:8000/api/v1"

# Create sample images for demonstration
def create_sample_image(color, filename):
    """Create a simple colored image for demonstration"""
    img = Image.new('RGB', (800, 600), color=color)
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def demo_vehicle_with_images():
    print("🚗 Vehicle + Image Upload Demo")
    print("=" * 40)
    
    # Step 1: Register admin user
    print("\n1. Registering admin user...")
    admin_data = {
        "username": "demo_admin",
        "email": "demo@example.com",
        "password": "demopass123",
        "password_confirm": "demopass123",
        "first_name": "Demo",
        "last_name": "Admin",
        "role": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=admin_data)
    if response.status_code == 201:
        admin_token = response.json()['token']
        print("✅ Admin registered successfully")
    else:
        print(f"❌ Admin registration failed: {response.status_code}")
        print(response.text)
        return
    
    # Step 2: Create sample images
    print("\n2. Creating sample images...")
    image1 = create_sample_image('red', 'front_view.jpg')
    image2 = create_sample_image('blue', 'side_view.jpg')
    image3 = create_sample_image('green', 'interior.jpg')
    print("✅ Sample images created")
    
    # Step 3: Upload vehicle with images
    print("\n3. Creating vehicle with images...")
    
    # Prepare form data
    vehicle_data = {
        'title': 'Demo Mercedes E350e',
        'year': '2018',
        'price': '16000',
        'fuel_type': 'hybrid_electric',
        'transmission': 'automatic',
        'mileage': '55,000 miles',
        'body_type': 'saloon',
        'color': 'Silver',
        'engine': '2.0L Hybrid Turbo',
        'description': 'Demo vehicle created via API with multiple images',
        'features': '["Premium Package", "Navigation", "Heated Seats", "Sunroof"]'
    }
    
    # Prepare files
    files = {
        'uploaded_images': [
            ('front_view.jpg', image1, 'image/jpeg'),
            ('side_view.jpg', image2, 'image/jpeg'),
            ('interior.jpg', image3, 'image/jpeg')
        ]
    }
    
    headers = {
        'Authorization': f'Token {admin_token}'
    }
    
    # Send multipart request
    response = requests.post(
        f"{BASE_URL}/vehicles/",
        data=vehicle_data,
        files=files,
        headers=headers
    )
    
    if response.status_code == 201:
        vehicle = response.json()
        print("✅ Vehicle created successfully!")
        print(f"   Vehicle ID: {vehicle['id']}")
        print(f"   Title: {vehicle['title']}")
        print(f"   Images uploaded: {len(vehicle['images'])}")
        
        # Display image URLs
        for i, img in enumerate(vehicle['images'], 1):
            print(f"   Image {i}: {img['image_url']}")
            print(f"     Primary: {img['is_primary']}")
        
        return vehicle['id']
    else:
        print(f"❌ Vehicle creation failed: {response.status_code}")
        print(response.text)
        return None

def demo_update_vehicle_images(vehicle_id, admin_token):
    """Demo updating a vehicle with additional images"""
    print(f"\n4. Adding more images to vehicle {vehicle_id}...")
    
    # Create additional sample image
    image4 = create_sample_image('yellow', 'engine.jpg')
    
    files = {
        'uploaded_images': [
            ('engine.jpg', image4, 'image/jpeg')
        ]
    }
    
    vehicle_data = {
        'description': 'Updated vehicle with additional engine photo'
    }
    
    headers = {
        'Authorization': f'Token {admin_token}'
    }
    
    response = requests.put(
        f"{BASE_URL}/vehicles/{vehicle_id}/",
        data=vehicle_data,
        files=files,
        headers=headers
    )
    
    if response.status_code == 200:
        vehicle = response.json()
        print("✅ Vehicle updated with additional images!")
        print(f"   Total images now: {len(vehicle['images'])}")
    else:
        print(f"❌ Vehicle update failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    try:
        # Note: This requires the Django server to be running
        vehicle_id = demo_vehicle_with_images()
        
        print("\n" + "=" * 40)
        print("🎉 Demo completed successfully!")
        print("\nKey Points:")
        print("• Vehicle data and images sent in single request")
        print("• Uses multipart/form-data encoding")
        print("• First image automatically set as primary")
        print("• Images uploaded to Cloudinary")
        print("• Returns complete vehicle data with image URLs")
        
        if vehicle_id:
            print(f"\nView your vehicle: {BASE_URL}/vehicles/{vehicle_id}/")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure Django server is running")
        print("   Run: python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {e}")
        
    print("\n" + "=" * 40)
    print("To test manually:")
    print("1. Use Postman with 'Create Vehicle with Images' request")
    print("2. Set body type to 'form-data'")
    print("3. Add text fields for vehicle data")
    print("4. Add file fields for 'uploaded_images'")
    print("5. Select multiple image files")
    print("6. Send request with admin token") 