# Deploying Vehicle Management API to Render

This guide will help you deploy your Django REST API to Render.

## Prerequisites

1. ✅ GitHub repository connected to Render (already done)
2. Cloudinary account for image uploads
3. PostgreSQL database (Render provides this)

## Step-by-Step Deployment

### 1. Create a Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository: `drive-x-auto`
4. Configure the service:
   - **Name**: `vehicle-management-api` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `vehicle_management`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn vehicle_management.wsgi:application`

### 2. Create a PostgreSQL Database

1. In Render Dashboard, click "New +" → "PostgreSQL"
2. Configure the database:
   - **Name**: `vehicle-management-db` (or your preferred name)
   - **Region**: Same as your web service
   - **PostgreSQL Version**: Latest
   - **Plan**: Free (for testing) or paid plan

### 3. Configure Environment Variables

In your web service settings, add these environment variables:

#### Required Variables:
```
SECRET_KEY=your-super-secret-django-key-here
DEBUG=False
DATABASE_URL=[Render will auto-populate this when you connect the database]
```

#### Cloudinary Variables (Required for image uploads):
```
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
```

#### Optional Variables:
```
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
```

### 4. Connect Database to Web Service

1. In your web service settings, scroll to "Environment"
2. Click "Add Environment Variable"
3. For the database connection, Render will automatically provide `DATABASE_URL`
4. Or manually connect by going to your database → "Connections" → "Connect to" your web service

### 5. Set up Cloudinary (Image Upload Service)

1. Sign up at [Cloudinary](https://cloudinary.com/)
2. Get your credentials from the Dashboard
3. Add the Cloudinary environment variables to your Render service

### 6. Deploy

1. Click "Create Web Service" or "Deploy Latest Commit"
2. Render will:
   - Clone your repository
   - Run `pip install -r requirements.txt`
   - Run `python manage.py collectstatic --no-input`
   - Run `python manage.py migrate`
   - Start your application with Gunicorn

### 7. Test Your Deployment

Once deployed, your API will be available at: `https://your-app-name.onrender.com`

Test these endpoints:
- `GET /api/auth/` - Authentication endpoints
- `GET /api/vehicles/` - Vehicle management endpoints
- `GET /admin/` - Django admin panel

## Important Notes

### Database Migrations
- The build script automatically runs migrations
- For future updates, migrations will run automatically on each deployment

### Static Files
- Static files are handled by WhiteNoise
- CSS/JS for Django admin will work automatically

### Environment Variables
- Never commit secrets to your repository
- Use Render's environment variable system
- Generate a new `SECRET_KEY` for production

### CORS Configuration
- Update `CORS_ALLOWED_ORIGINS` in settings.py with your frontend domain
- Currently configured for development; update for production

### Security
- HTTPS is automatically provided by Render
- Security headers are configured in settings.py
- DEBUG is set to False for production

## Troubleshooting

### Build Fails
- Check the build logs in Render dashboard
- Ensure all requirements are in `requirements.txt`
- Verify `build.sh` has correct permissions

### Database Connection Issues
- Ensure `DATABASE_URL` is set correctly
- Check that the database and web service are in the same region

### Static Files Not Loading
- Verify `STATIC_ROOT` and `STATIC_URL` settings
- Check that `collectstatic` runs successfully

### Image Uploads Not Working
- Verify Cloudinary credentials
- Check Cloudinary usage limits
- Ensure proper CORS configuration

## Next Steps

1. Set up a custom domain (optional)
2. Configure monitoring and alerts
3. Set up CI/CD for automatic deployments
4. Scale your service based on traffic

## API Documentation

Your API endpoints will be:

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Vehicles
- `GET /api/vehicles/` - List vehicles
- `POST /api/vehicles/` - Create vehicle
- `GET /api/vehicles/{id}/` - Get vehicle details
- `PUT /api/vehicles/{id}/` - Update vehicle
- `DELETE /api/vehicles/{id}/` - Delete vehicle

### Admin
- `/admin/` - Django admin panel

Remember to replace `your-app-name` with your actual Render service name! 