from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.exceptions import ValidationError

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        description="Obtain a pair of JWT tokens (access and refresh)",
        request=CustomTokenObtainPairSerializer,
        responses={200: {"description": "JWT Tokens", "content": {"application/json": {"example": {"access": "your-access-token", "refresh": "your-refresh-token"}}}},
        400: {"description": "Validation Error", "content": {"application/json": {"example": {"detail": "Invalid credentials"}}}}},
        parameters=[
            OpenApiParameter(
                name="username",
                type=OpenApiTypes.STR,
                location="form",
                description="Username of the user"
            ),
            OpenApiParameter(
                name="password",
                type=OpenApiTypes.STR,
                location="form",
                description="Password of the user"
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        description="Register a new user with role selection (HR or Seeker)",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: {
                "description": "Validation Error", 
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Invalid role or username already exists"
                        }
                    }
                }
            }
        },
        parameters=[
            OpenApiParameter(
                name="email",
                type=OpenApiTypes.STR,
                location="form",
                description="Email of the new user"
            ),
            OpenApiParameter(
                name="username",
                type=OpenApiTypes.STR,
                location="form",
                description="Username of the new user"
            ),
            OpenApiParameter(
                name="password",
                type=OpenApiTypes.STR,
                location="form",
                description="Password for the new user"
            ),
            OpenApiParameter(
                name="role",
                type=OpenApiTypes.STR,
                location="form",
                description="Role of the new user: 'seeker' or 'hr'"
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        role = request.data.get('role')
        if role not in ['seeker', 'hr']:
            raise ValidationError({'role': 'Role must be either "seeker" or "hr"'})
        return super().post(request, *args, **kwargs)