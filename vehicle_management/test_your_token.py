#!/usr/bin/env python
"""
Test your specific token to debug vehicle creation issue
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_your_token():
    print("🔍 Testing Your Token")
    print("=" * 40)
    
    # Get token from user
    token = input("Paste your token here: ").strip()
    
    if not token:
        print("❌ No token provided")
        return
    
    print(f"Token received: {token[:20]}...{token[-10:] if len(token) > 30 else token}")
    
    # Test different formats
    test_formats = [
        f"Token {token}",
        f"Bearer {token}",
        token
    ]
    
    for i, auth_header in enumerate(test_formats, 1):
        print(f"\n{i}. Testing format: {auth_header[:50]}...")
        
        headers = {"Authorization": auth_header}
        
        # Test profile first
        try:
            response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
            print(f"   Profile Status: {response.status_code}")
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"   ✅ Authentication SUCCESS!")
                print(f"   User: {user_data.get('username')}")
                print(f"   Role: {user_data.get('role')}")
                
                # Check if admin
                if user_data.get('role') != 'admin':
                    print(f"   ⚠️  WARNING: Role is '{user_data.get('role')}', need 'admin' for vehicle creation")
                    continue
                
                # Test vehicle creation with JSON
                print(f"\n   Testing vehicle creation (JSON)...")
                vehicle_data = {
                    "title": "Token Test Vehicle",
                    "year": 2021,
                    "price": 20000,
                    "fuel_type": "petrol",
                    "transmission": "automatic",
                    "mileage": "30000 miles",
                    "body_type": "sedan",
                    "color": "Blue",
                    "engine": "2.0L",
                    "description": "Test vehicle with your token",
                    "features": ["Test Feature"]
                }
                
                json_headers = {
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
                
                response = requests.post(f"{BASE_URL}/vehicles/", 
                                       json=vehicle_data, 
                                       headers=json_headers)
                
                print(f"   Vehicle Creation Status: {response.status_code}")
                
                if response.status_code == 201:
                    vehicle = response.json()
                    print(f"   ✅ VEHICLE CREATION SUCCESS!")
                    print(f"   Vehicle ID: {vehicle.get('id')}")
                    print(f"   Title: {vehicle.get('title')}")
                    
                    # Test form-data
                    print(f"\n   Testing vehicle creation (Form-Data)...")
                    form_data = {
                        'title': 'Form Data Test Vehicle',
                        'year': '2022',
                        'price': '25000',
                        'fuel_type': 'electric',
                        'transmission': 'automatic',
                        'mileage': '10000 miles',
                        'body_type': 'hatchback',
                        'color': 'White',
                        'engine': 'Electric Motor',
                        'description': 'Form data test vehicle',
                        'features': '["Electric", "Eco-friendly"]'
                    }
                    
                    form_headers = {"Authorization": auth_header}
                    
                    response = requests.post(f"{BASE_URL}/vehicles/",
                                           data=form_data,
                                           headers=form_headers)
                    
                    print(f"   Form-Data Status: {response.status_code}")
                    
                    if response.status_code == 201:
                        print(f"   ✅ FORM-DATA SUCCESS!")
                        vehicle = response.json()
                        print(f"   Vehicle ID: {vehicle.get('id')}")
                    else:
                        print(f"   ❌ Form-data failed: {response.text}")
                    
                    # Provide exact Postman instructions
                    print(f"\n" + "=" * 50)
                    print("🎯 FOR POSTMAN - Use exactly this:")
                    print(f"Authorization: {auth_header}")
                    print("\nFor JSON requests:")
                    print("- Headers: Authorization + Content-Type: application/json")
                    print("- Body: raw → JSON")
                    print("\nFor Form-Data requests (with images):")
                    print("- Headers: Authorization ONLY (remove Content-Type)")
                    print("- Body: form-data → add fields")
                    return
                    
                else:
                    print(f"   ❌ Vehicle creation failed: {response.text}")
            else:
                print(f"   ❌ Authentication failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n❌ No working authentication format found")

if __name__ == "__main__":
    try:
        test_your_token()
    except KeyboardInterrupt:
        print("\nTest cancelled")
    except Exception as e:
        print(f"Error: {e}") 