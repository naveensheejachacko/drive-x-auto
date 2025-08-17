#!/usr/bin/env python
"""
Quick authentication test - run this to debug your token issue
"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

def quick_test():
    print("🔍 Quick Authentication Test")
    print("=" * 40)
    
    # Get your token by logging in
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    # Login
    print(f"\n1. Logging in user: {username}")
    response = requests.post(f"{BASE_URL}/auth/login/", json={
        "username": username,
        "password": password
    })
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return
    
    token = response.json().get('token')
    print(f"✅ Login successful!")
    print(f"Token: {token}")
    
    # Test profile
    print(f"\n2. Testing profile endpoint...")
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
    
    if response.status_code == 200:
        user = response.json()
        print(f"✅ Profile works!")
        print(f"Username: {user['username']}")
        print(f"Role: {user['role']}")
        
        if user['role'] != 'admin':
            print("⚠️  WARNING: You need admin role to create vehicles!")
            return
    else:
        print(f"❌ Profile failed: {response.text}")
        return
    
    # Test simple vehicle creation
    print(f"\n3. Testing vehicle creation...")
    vehicle_data = {
        "title": "Quick Test Car",
        "year": 2020,
        "price": 15000,
        "fuel_type": "petrol",
        "transmission": "automatic",
        "mileage": "50000 miles",
        "body_type": "sedan",
        "color": "Red",
        "engine": "2.0L",
        "description": "Quick test vehicle",
        "features": ["Test"]
    }
    
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{BASE_URL}/vehicles/", json=vehicle_data, headers=headers)
    
    if response.status_code == 201:
        vehicle = response.json()
        print(f"✅ Vehicle created successfully!")
        print(f"Vehicle ID: {vehicle['id']}")
        print(f"Title: {vehicle['title']}")
    else:
        print(f"❌ Vehicle creation failed: {response.text}")
    
    print(f"\n" + "=" * 40)
    print("For Postman, use exactly this:")
    print(f"Authorization: Token {token}")
    print("(Copy the line above exactly as shown)")

if __name__ == "__main__":
    try:
        quick_test()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Django server is running: python manage.py runserver") 