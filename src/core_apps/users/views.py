from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from core_apps.users.renderers import UserJSONRenderer
from core_apps.users.serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationAPISerializer,
)


class UserRegistrationAPI(APIView):
    """API for User Registration"""

    renderer_classes = [UserJSONRenderer]

    def post(self, request):
        serializer = UserRegistrationAPISerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                token = CustomTokenObtainPairSerializer.get_token(user)
                return Response(
                    {
                        "status": "success",
                        "refresh": str(token),
                        "access": str(token.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"status": "error", "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as ve:
            return Response(
                {"status": "error", "detail": ve.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except IntegrityError as ie:
            return Response(
                {
                    "status": "error",
                    "detail": "A user with this username already exists!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "error", "detail": "Something went wrong at our end!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserLoginAPI(APIView):
    """API for User Login"""

    renderer_classes = [UserJSONRenderer]

    def post(self, request):
        # Credential can be either "email" or "username"
        credential = request.data.get("credential", None)
        password = request.data.get("password", None)

        if not credential:
            return Response(
                {"status": "error", "detail": "email or username is not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not password:
            return Response(
                {"status": "error", "detail": "password is not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Custom auth backend is used.
        user = authenticate(
            request=request, email=credential, username=credential, password=password
        )
        if user:
            token = CustomTokenObtainPairSerializer.get_token(user)
            return Response(
                {
                    "status": "success",
                    "refresh": str(token),
                    "access": str(token.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "status": "error",
                "detail": {
                    "non_field_errors": ["Username, Email or password is incorrect"]
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserLogOutAPIView(APIView):
    """API for User Logout"""

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"status": "error", "detail": "Refresh Token is not provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"status": "success", "detail": "User logged out successfully."},
                status=status.HTTP_200_OK,
            )
        except TokenError as e:
            return Response(
                {"status": "error", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"status": "error", "detail": "Something went wrong at our end!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserTokenObtainPairView(APIView):
    """API to get access and refresh token."""

    serializer_class = CustomTokenObtainPairSerializer
    renderer_classes = [UserJSONRenderer]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
