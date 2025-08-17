#!/usr/bin/env python
"""
Debug script to test authentication and identify token issues.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_authentication():
    print("🔍 Authentication Debug Tool")
    print("=" * 50)
    
    # Step 1: Register a test admin user
    print("\n1. Registering test admin user...")
    admin_data = {
        "username": "debug_admin",
        "email": "debug@test.com", 
        "password": "debugpass123",
        "password_confirm": "debugpass123",
        "first_name": "Debug",
        "last_name": "Admin",
        "role": "admin"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", 
                               json=admin_data,
                               headers={"Content-Type": "application/json"})
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 201:
            token = response.json().get('token')
            print(f"   ✅ Registration successful")
            print(f"   Token: {token}")
            print(f"   Token length: {len(token) if token else 'None'}")
            return token
        else:
            print(f"   ❌ Registration failed")
            print(f"   Response: {response.text}")
            
            # Try to login if user already exists
            print("\n   Trying to login instead...")
            login_data = {
                "username": "debug_admin",
                "password": "debugpass123"
            }
            response = requests.post(f"{BASE_URL}/auth/login/", 
                                   json=login_data,
                                   headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                token = response.json().get('token')
                print(f"   ✅ Login successful")
                print(f"   Token: {token}")
                return token
            else:
                print(f"   ❌ Login also failed: {response.text}")
                return None
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_token_formats(token):
    """Test different token formats to identify the issue"""
    print(f"\n2. Testing different token formats...")
    print(f"   Using token: {token}")
    
    test_cases = [
        ("Token " + token, "Standard Token format"),
        ("Bearer " + token, "Bearer format (wrong)"),
        (token, "Raw token (wrong)"),
        ("token " + token, "Lowercase token (wrong)"),
    ]
    
    for auth_header, description in test_cases:
        print(f"\n   Testing: {description}")
        print(f"   Header: Authorization: {auth_header}")
        
        headers = {"Authorization": auth_header}
        
        try:
            # Test with profile endpoint first (simpler)
            response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
            print(f"   Profile endpoint - Status: {response.status_code}")
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"   ✅ Success! User: {user_data.get('username')} (Role: {user_data.get('role')})")
                return auth_header  # Return the working format
            else:
                print(f"   ❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

def test_vehicle_creation(working_auth_header):
    """Test vehicle creation with working auth header"""
    print(f"\n3. Testing vehicle creation...")
    
    # Test with JSON first (no images)
    print("\n   Testing JSON vehicle creation...")
    vehicle_data = {
        "title": "Debug Test Vehicle",
        "year": 2020,
        "price": 15000,
        "fuel_type": "petrol",
        "transmission": "automatic", 
        "mileage": "50,000 miles",
        "body_type": "sedan",
        "color": "Blue",
        "engine": "2.0L",
        "description": "Debug test vehicle",
        "features": ["Test Feature"]
    }
    
    headers = {
        "Authorization": working_auth_header,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/vehicles/", 
                               json=vehicle_data, 
                               headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            vehicle = response.json()
            print(f"   ✅ Vehicle created successfully!")
            print(f"   Vehicle ID: {vehicle.get('id')}")
            print(f"   Title: {vehicle.get('title')}")
            return vehicle.get('id')
        else:
            print(f"   ❌ Failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_form_data_upload(working_auth_header):
    """Test form-data upload (with images)"""
    print(f"\n4. Testing form-data vehicle creation...")
    
    # Create a simple test image
    from io import BytesIO
    try:
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        has_pil = True
    except ImportError:
        print("   PIL not available, testing without images...")
        has_pil = False
    
    vehicle_data = {
        'title': 'Debug Form Data Vehicle',
        'year': '2021',
        'price': '18000',
        'fuel_type': 'electric',
        'transmission': 'automatic',
        'mileage': '30,000 miles',
        'body_type': 'hatchback',
        'color': 'Green',
        'engine': 'Electric Motor',
        'description': 'Debug form-data test vehicle',
        'features': '["Electric", "Eco-friendly"]'
    }
    
    headers = {"Authorization": working_auth_header}
    
    if has_pil:
        files = {'uploaded_images': ('test.jpg', img_bytes, 'image/jpeg')}
    else:
        files = {}
    
    try:
        response = requests.post(f"{BASE_URL}/vehicles/",
                               data=vehicle_data,
                               files=files,
                               headers=headers)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            vehicle = response.json()
            print(f"   ✅ Form-data vehicle created successfully!")
            print(f"   Vehicle ID: {vehicle.get('id')}")
            print(f"   Title: {vehicle.get('title')}")
            if has_pil:
                print(f"   Images: {len(vehicle.get('images', []))}")
        else:
            print(f"   ❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    try:
        # Test authentication
        token = test_authentication()
        if not token:
            print("\n❌ Cannot proceed without valid token")
            return
        
        # Test token formats
        working_auth = test_token_formats(token)
        if not working_auth:
            print("\n❌ No working authentication format found")
            return
        
        print(f"\n✅ Working authentication format: {working_auth}")
        
        # Test vehicle creation
        test_vehicle_creation(working_auth)
        test_form_data_upload(working_auth)
        
        print("\n" + "=" * 50)
        print("🎉 Debug complete!")
        print("\nFor Postman:")
        print(f"1. Use Authorization header: {working_auth}")
        print("2. For form-data, don't include Content-Type header")
        print("3. Make sure you have admin role")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure Django server is running")
        print("   Run: python manage.py runserver")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 