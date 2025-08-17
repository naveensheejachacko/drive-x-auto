#!/usr/bin/env python
"""
Simple test script to verify API endpoints are working correctly.
Run this after starting the development server.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
ADMIN_USER = {
    "username": "admin_test",
    "email": "admin@test.com",
    "password": "adminpass123",
    "password_confirm": "adminpass123",
    "first_name": "Admin",
    "last_name": "Test",
    "role": "admin"
}

REGULAR_USER = {
    "username": "user_test",
    "email": "user@test.com",
    "password": "userpass123",
    "password_confirm": "userpass123",
    "first_name": "User",
    "last_name": "Test",
    "role": "user"
}

SAMPLE_VEHICLE = {
    "title": "Test Mercedes Benz E350e",
    "year": 2017,
    "price": 14000,
    "fuel_type": "hybrid_electric",
    "transmission": "automatic",
    "mileage": "60,000 miles",
    "body_type": "saloon",
    "color": "Black",
    "engine": "2.0L Hybrid",
    "description": "Test vehicle for API verification",
    "features": [
        "Clean Hybrid Electric",
        "Excellent Condition",
        "Navigation System"
    ]
}

def test_api():
    print("🚀 Starting API Test...")
    
    # Test 1: API Root
    print("\n1. Testing API Root...")
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print("✅ API Root accessible")
        print(f"   Response: {response.json()['message']}")
    else:
        print(f"❌ API Root failed: {response.status_code}")
        return
    
    # Test 2: Register Admin User
    print("\n2. Registering Admin User...")
    response = requests.post(f"{BASE_URL}/auth/register/", 
                           json=ADMIN_USER,
                           headers={"Content-Type": "application/json"})
    if response.status_code == 201:
        admin_token = response.json()['token']
        print("✅ Admin user registered successfully")
    else:
        print(f"❌ Admin registration failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return
    
    # Test 3: Register Regular User
    print("\n3. Registering Regular User...")
    response = requests.post(f"{BASE_URL}/auth/register/", 
                           json=REGULAR_USER,
                           headers={"Content-Type": "application/json"})
    if response.status_code == 201:
        user_token = response.json()['token']
        print("✅ Regular user registered successfully")
    else:
        print(f"❌ User registration failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return
    
    # Test 4: Create Vehicle (Admin)
    print("\n4. Creating Vehicle (Admin)...")
    headers = {
        "Authorization": f"Token {admin_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{BASE_URL}/vehicles/", 
                           json=SAMPLE_VEHICLE, headers=headers)
    if response.status_code == 201:
        vehicle_id = response.json()['id']
        print(f"✅ Vehicle created successfully (ID: {vehicle_id})")
    else:
        print(f"❌ Vehicle creation failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return
    
    # Test 5: List Vehicles
    print("\n5. Listing Vehicles...")
    headers = {"Authorization": f"Token {user_token}"}
    response = requests.get(f"{BASE_URL}/vehicles/", headers=headers)
    if response.status_code == 200:
        vehicles = response.json()['results']
        print(f"✅ Vehicles listed successfully ({len(vehicles)} found)")
    else:
        print(f"❌ Vehicle listing failed: {response.status_code}")
    
    # Test 6: Get Vehicle Details
    print("\n6. Getting Vehicle Details...")
    response = requests.get(f"{BASE_URL}/vehicles/{vehicle_id}/", headers=headers)
    if response.status_code == 200:
        vehicle = response.json()
        print(f"✅ Vehicle details retrieved: {vehicle['title']}")
    else:
        print(f"❌ Vehicle details failed: {response.status_code}")
    
    # Test 7: Add to Wishlist
    print("\n7. Adding to Wishlist...")
    response = requests.post(f"{BASE_URL}/vehicles/{vehicle_id}/wishlist/toggle/", 
                           headers=headers)
    if response.status_code in [200, 201]:
        print("✅ Vehicle added to wishlist")
    else:
        print(f"❌ Wishlist operation failed: {response.status_code}")
    
    # Test 8: Get Wishlist
    print("\n8. Getting User Wishlist...")
    response = requests.get(f"{BASE_URL}/vehicles/wishlist/", headers=headers)
    if response.status_code == 200:
        wishlist = response.json()['results']
        print(f"✅ Wishlist retrieved ({len(wishlist)} items)")
    else:
        print(f"❌ Wishlist retrieval failed: {response.status_code}")
    
    # Test 9: Gallery
    print("\n9. Getting Gallery...")
    response = requests.get(f"{BASE_URL}/vehicles/gallery/?limit=10", headers=headers)
    if response.status_code == 200:
        gallery = response.json()
        print(f"✅ Gallery retrieved ({len(gallery)} images)")
    else:
        print(f"❌ Gallery retrieval failed: {response.status_code}")
    
    # Test 10: User Profile
    print("\n10. Getting User Profile...")
    response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
    if response.status_code == 200:
        profile = response.json()
        print(f"✅ Profile retrieved: {profile['username']} ({profile['role']})")
    else:
        print(f"❌ Profile retrieval failed: {response.status_code}")
    
    print("\n🎉 API Test Complete!")
    print("\nTo run this test:")
    print("1. Start the development server: python manage.py runserver")
    print("2. Run this script: python test_api.py")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Django server is running on localhost:8000")
        print("   Run: python manage.py runserver")
    except Exception as e:
        print(f"❌ Unexpected error: {e}") 