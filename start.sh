#!/bin/bash
# Startup script for production deployment
# Sets default PORT if not provided by the hosting platform

export PORT=${PORT:-8000}

echo "📚 Starting Library Management System..."

# Run database migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Setup user groups (Administrators, Members)
python manage.py setup_groups

# Seed sample books (creates only if database is empty)
python manage.py seed_books

# Create admin user (only if not exists)
echo "👤 Checking admin user..."
python manage.py shell -c "
from apps.accounts.models import User
from django.contrib.auth.models import Group

if not User.objects.filter(email='admin123@gmail.com').exists():
    admin = User.objects.create_superuser(
        email='admin123@gmail.com',
        password='Admin@123',
        username='admin123',
        first_name='Admin',
        last_name='User'
    )
    admin_group, _ = Group.objects.get_or_create(name='Administrators')
    admin.groups.add(admin_group)
    print('✓ Admin user created successfully')
else:
    print('✓ Admin user already exists')
"

# Start the web server
echo "🚀 Starting Gunicorn server on port $PORT..."
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
