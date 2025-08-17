# Vehicle Management API

A comprehensive Django REST API for vehicle management with role-based access control, image handling via Cloudinary, and wishlist functionality.

## Features

- **Role-based Authentication**: Admin and User roles with different permissions
- **Vehicle CRUD Operations**: Full create, read, update, delete functionality
- **Image Management**: Upload and manage vehicle images using Cloudinary
- **Wishlist System**: Users can add/remove vehicles from their wishlist
- **Gallery Feed**: Random vehicle images for browsing
- **Advanced Filtering**: Search and filter vehicles by various criteria
- **PostgreSQL Database**: Robust data storage
- **RESTful API**: Clean, well-documented API endpoints

## Tech Stack

- **Backend**: Django 5.2.5, Django REST Framework 3.16.1
- **Database**: PostgreSQL (with psycopg2-binary)
- **Image Storage**: Cloudinary
- **Authentication**: Token-based authentication
- **Environment Management**: python-decouple

## Installation & Setup

### 1. Clone and Setup Virtual Environment

```bash
git clone <repository-url>
cd vehicle_management
python3 -m venv vehicle_app_env
source vehicle_app_env/bin/activate  # On Windows: vehicle_app_env\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration
DB_NAME=vehicle_management
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 4. Database Setup

```bash
# Create PostgreSQL database
createdb vehicle_management

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 5. Run the Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/v1/`

## API Documentation

### Base URL
```
http://localhost:8000/api/v1/
```

### Authentication Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| GET | `/` | API root with endpoint overview | Public |
| POST | `/auth/register/` | User registration | Public |
| POST | `/auth/login/` | User login | Public |
| POST | `/auth/logout/` | User logout | Authenticated |
| GET | `/auth/profile/` | Get user profile | Authenticated |

### Vehicle Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| GET | `/vehicles/` | List all vehicles (with filtering) | Authenticated |
| POST | `/vehicles/` | Create new vehicle | Admin only |
| GET | `/vehicles/{id}/` | Get vehicle details | Authenticated |
| PUT | `/vehicles/{id}/` | Update vehicle | Owner/Admin |
| DELETE | `/vehicles/{id}/` | Delete vehicle (soft delete) | Owner/Admin |

### Image Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| GET | `/vehicles/{id}/images/` | List vehicle images | Authenticated |
| POST | `/vehicles/{id}/images/` | Upload vehicle image | Owner/Admin |
| DELETE | `/vehicles/{id}/images/{image_id}/delete/` | Delete vehicle image | Owner/Admin |

### Gallery & Wishlist Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| GET | `/vehicles/gallery/` | Get random vehicle images | Authenticated |
| GET | `/vehicles/wishlist/` | Get user's wishlist | Authenticated |
| POST | `/vehicles/wishlist/` | Add vehicle to wishlist | Authenticated |
| POST | `/vehicles/{id}/wishlist/toggle/` | Toggle vehicle in wishlist | Authenticated |
| DELETE | `/vehicles/{id}/wishlist/remove/` | Remove from wishlist | Authenticated |

### Admin Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| GET | `/vehicles/stats/` | Get vehicle statistics | Admin only |

## Sample API Usage

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User",
    "role": "user"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### 3. Create a Vehicle (Admin only)

```bash
curl -X POST http://localhost:8000/api/v1/vehicles/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "title": "Mercedes Benz E350e",
    "year": 2017,
    "price": 14000,
    "fuel_type": "hybrid_electric",
    "transmission": "automatic",
    "mileage": "60,000 miles",
    "body_type": "saloon",
    "color": "Black",
    "engine": "2.0L Hybrid",
    "description": "Mercedes Benz E350e 2017 Hybrid Electric...",
    "features": [
      "Clean Hybrid Electric",
      "Excellent Condition",
      "Navigation System"
    ]
  }'
```

### 4. Search Vehicles

```bash
curl -X GET "http://localhost:8000/api/v1/vehicles/?search=Mercedes&fuel_type=hybrid_electric&min_price=10000" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Vehicle Data Model

### Sample Vehicle JSON

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
  "description": "Mercedes Benz E350e 2017 Hybrid Electric...",
  "features": [
    "Clean Hybrid Electric",
    "Excellent Condition",
    "Navigation System"
  ],
  "images": [
    {
      "id": 1,
      "image_url": "https://res.cloudinary.com/...",
      "is_primary": true,
      "uploaded_at": "2024-01-01T10:00:00Z"
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

## Filtering Options

### Query Parameters

- `search`: Search in title, description, color, fuel_type, body_type
- `fuel_type`: Filter by fuel type (petrol, diesel, electric, hybrid, hybrid_electric, gas)
- `body_type`: Filter by body type (sedan, saloon, hatchback, suv, coupe, etc.)
- `transmission`: Filter by transmission (manual, automatic, cvt)
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter
- `min_year`: Minimum year filter
- `max_year`: Maximum year filter

### Example with Filters

```
GET /api/v1/vehicles/?search=BMW&fuel_type=petrol&body_type=sedan&min_price=15000&max_price=25000&min_year=2015
```

## Postman Collection

Import the provided `Vehicle_Management_API.postman_collection.json` file into Postman for easy testing of all endpoints.

The collection includes:
- Environment variables for base URL and auth tokens
- Pre-request scripts for authentication
- Sample data for all endpoints
- Automated token management

## Permissions & Roles

### User Roles

1. **Admin**: Can create, update, delete any vehicle; access statistics
2. **User**: Can view vehicles, manage their wishlist, view gallery

### Permission Matrix

| Action | Admin | User |
|--------|-------|------|
| View vehicles | ✅ | ✅ |
| Create vehicle | ✅ | ❌ |
| Update own vehicle | ✅ | ❌ |
| Update any vehicle | ✅ | ❌ |
| Delete own vehicle | ✅ | ❌ |
| Delete any vehicle | ✅ | ❌ |
| Upload vehicle images | ✅ | ❌ |
| Manage wishlist | ✅ | ✅ |
| View gallery | ✅ | ✅ |
| View statistics | ✅ | ❌ |

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `200`: Success
- `201`: Created
- `204`: No Content (for deletions)
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (authentication required)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `500`: Internal Server Error

### Sample Error Response

```json
{
  "error": "You don't have permission to perform this action.",
  "detail": "Admin access required for creating vehicles."
}
```

## Development

### Running Tests

```bash
python manage.py test
```

### Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to manage data through a web interface.

### Code Structure

```
vehicle_management/
├── authentication/          # User management and auth
├── vehicles/               # Vehicle CRUD and related functionality
├── vehicle_management/     # Project settings
├── .env                   # Environment variables
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## Production Deployment

1. Set `DEBUG=False` in environment variables
2. Configure allowed hosts
3. Set up proper PostgreSQL database
4. Configure Cloudinary for production
5. Use environment variables for all sensitive data
6. Set up proper CORS settings for your frontend domain

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License. 