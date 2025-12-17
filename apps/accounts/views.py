"""
Accounts app views.
"""
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UserAdminSerializer
)
from .permissions import IsAdministrator

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(operation_id="UserLogin", operation_summary="User Login", operation_description="Authenticate with email and password to get access and refresh tokens.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(operation_id="RefreshToken", operation_summary="Refresh Access Token", operation_description="Get a new access token using a valid refresh token.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint.
    Public access - creates a new Member user.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id="RegisterMember", operation_summary="Register New Member", operation_description="Create a new member account.")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Current user profile endpoint.
    GET: Retrieve current user's profile
    PUT/PATCH: Update current user's profile
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(operation_id="GetProfile", operation_summary="Get My Profile")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_id="UpdateProfile", operation_summary="Update My Profile")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(operation_id="PatchProfile", operation_summary="Partial Update My Profile")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    """
    Admin endpoint for managing users.
    Only Administrators can access.
    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdministrator]
    filter_backends = []  # Disable search/ordering/pagination in Swagger
    pagination_class = None  # Simple list

    def get_queryset(self):
        return User.objects.prefetch_related('groups').order_by('-created_at')

    @swagger_auto_schema(operation_id="AdminListUsers", operation_summary="List All Users (Admin)")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_id="AdminCreateUser", operation_summary="Create User (Admin)")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_id="AdminGetUser", operation_summary="Get User Details (Admin)")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_id="AdminUpdateUser", operation_summary="Update User (Admin)")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_id="AdminPatchUser", operation_summary="Partial Update User (Admin)")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_id="AdminDeleteUser", operation_summary="Delete User (Admin)")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
