# Vehicle + Image Upload Examples

## Method 1: Using multipart/form-data (Recommended)

### 📤 Single Request with Vehicle Data + Images

```bash
curl -X POST http://localhost:8000/api/v1/vehicles/ \
  -H "Authorization: Token YOUR_ADMIN_TOKEN" \
  -F "title=Mercedes Benz E350e" \
  -F "year=2017" \
  -F "price=14000" \
  -F "fuel_type=hybrid_electric" \
  -F "transmission=automatic" \
  -F "mileage=60,000 miles" \
  -F "body_type=saloon" \
  -F "color=Black" \
  -F "engine=2.0L Hybrid" \
  -F "description=Mercedes Benz E350e 2017 Hybrid Electric. Excellent condition." \
  -F "features=[\"Clean Hybrid Electric\", \"Excellent Condition\", \"Navigation System\"]" \
  -F "uploaded_images=@/path/to/image1.jpg" \
  -F "uploaded_images=@/path/to/image2.jpg" \
  -F "uploaded_images=@/path/to/image3.jpg"
```

### 🔧 JavaScript/Frontend Example

```javascript
const formData = new FormData();

// Vehicle data
formData.append('title', 'Mercedes Benz E350e');
formData.append('year', '2017');
formData.append('price', '14000');
formData.append('fuel_type', 'hybrid_electric');
formData.append('transmission', 'automatic');
formData.append('mileage', '60,000 miles');
formData.append('body_type', 'saloon');
formData.append('color', 'Black');
formData.append('engine', '2.0L Hybrid');
formData.append('description', 'Mercedes Benz E350e 2017 Hybrid Electric');
formData.append('features', JSON.stringify([
    "Clean Hybrid Electric",
    "Excellent Condition", 
    "Navigation System"
]));

// Multiple images
formData.append('uploaded_images', file1); // File object from input
formData.append('uploaded_images', file2);
formData.append('uploaded_images', file3);

// Send request
fetch('http://localhost:8000/api/v1/vehicles/', {
    method: 'POST',
    headers: {
        'Authorization': 'Token YOUR_ADMIN_TOKEN'
    },
    body: formData
})
.then(response => response.json())
.then(data => console.log('Vehicle created:', data));
```

### 📱 React Component Example

```jsx
import React, { useState } from 'react';

const VehicleUploadForm = () => {
    const [vehicleData, setVehicleData] = useState({
        title: '',
        year: '',
        price: '',
        fuel_type: '',
        transmission: '',
        mileage: '',
        body_type: '',
        color: '',
        engine: '',
        description: '',
        features: []
    });
    const [images, setImages] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        
        // Add vehicle data
        Object.keys(vehicleData).forEach(key => {
            if (key === 'features') {
                formData.append(key, JSON.stringify(vehicleData[key]));
            } else {
                formData.append(key, vehicleData[key]);
            }
        });
        
        // Add images
        images.forEach(image => {
            formData.append('uploaded_images', image);
        });
        
        try {
            const response = await fetch('/api/v1/vehicles/', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${localStorage.getItem('authToken')}`
                },
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log('Vehicle created successfully:', result);
            }
        } catch (error) {
            console.error('Upload failed:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit} encType="multipart/form-data">
            {/* Vehicle form fields */}
            <input 
                type="text" 
                placeholder="Vehicle Title"
                value={vehicleData.title}
                onChange={(e) => setVehicleData({...vehicleData, title: e.target.value})}
            />
            
            {/* Image upload */}
            <input 
                type="file" 
                multiple 
                accept="image/*"
                onChange={(e) => setImages(Array.from(e.target.files))}
            />
            
            <button type="submit">Create Vehicle with Images</button>
        </form>
    );
};
```

## Method 2: Postman Setup

### 📋 Postman Configuration

1. **Method**: POST
2. **URL**: `http://localhost:8000/api/v1/vehicles/`
3. **Headers**: 
   - `Authorization: Token YOUR_ADMIN_TOKEN`
4. **Body Type**: form-data
5. **Form Data**:
   ```
   title: Mercedes Benz E350e
   year: 2017
   price: 14000
   fuel_type: hybrid_electric
   transmission: automatic
   mileage: 60,000 miles
   body_type: saloon
   color: Black
   engine: 2.0L Hybrid
   description: Mercedes Benz E350e 2017 Hybrid Electric
   features: ["Clean Hybrid Electric", "Excellent Condition", "Navigation System"]
   uploaded_images: [File] image1.jpg
   uploaded_images: [File] image2.jpg
   uploaded_images: [File] image3.jpg
   ```

## 🔍 How It Works Internally

1. **Request Processing**: Django receives multipart/form-data
2. **Serializer Validation**: VehicleSerializer validates both data and images
3. **Vehicle Creation**: Vehicle record is created in database
4. **Image Processing**: Each image is:
   - Uploaded to Cloudinary
   - VehicleImage record created with Cloudinary URL
   - First image marked as primary
5. **Response**: Complete vehicle data with image URLs returned

## 📤 Response Format

```json
{
    "id": 1,
    "title": "Mercedes Benz E350e",
    "year": 2017,
    "price": "14000.00",
    "fuel_type": "hybrid_electric",
    "transmission": "automatic",
    "mileage": "60,000 miles",
    "body_type": "saloon",
    "color": "Black",
    "engine": "2.0L Hybrid",
    "description": "Mercedes Benz E350e 2017 Hybrid Electric",
    "features": [
        "Clean Hybrid Electric",
        "Excellent Condition",
        "Navigation System"
    ],
    "images": [
        {
            "id": 1,
            "image_url": "https://res.cloudinary.com/your-cloud/image/upload/v1234567890/abc123.jpg",
            "is_primary": true,
            "uploaded_at": "2024-01-01T10:00:00Z"
        },
        {
            "id": 2,
            "image_url": "https://res.cloudinary.com/your-cloud/image/upload/v1234567890/def456.jpg",
            "is_primary": false,
            "uploaded_at": "2024-01-01T10:00:01Z"
        }
    ],
    "is_wishlisted": false,
    "created_by": 1,
    "created_by_username": "admin",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z",
    "is_active": true
}
```

## ⚠️ Important Notes

1. **File Size Limits**: Configure in Django settings if needed
2. **Image Formats**: Cloudinary supports JPG, PNG, WebP, etc.
3. **Primary Image**: First uploaded image becomes primary automatically
4. **Error Handling**: Validation errors returned for both data and images
5. **Admin Only**: Only users with admin role can create vehicles

## 🔧 Alternative: JSON + Base64 (Not Recommended)

If you prefer JSON format, you could modify the serializer to accept base64 encoded images, but multipart/form-data is more efficient for file uploads. 