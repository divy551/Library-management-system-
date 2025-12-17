"""
Accounts app URL configuration.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    ProfileView,
    UserViewSet,
    CustomTokenObtainPairView,
    CustomTokenRefreshView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('me/', ProfileView.as_view(), name='profile'),
    # Admin user management
    path('', include(router.urls)),
]
