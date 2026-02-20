from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema, inline_serializer
from apps.utils import BaseResponse
from apps.user.api.serializers import LoginSerializer, RefreshTokenSerializer, LogoutSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        summary="Obtain access & refresh tokens",
        request=LoginSerializer,
        responses={
            200: inline_serializer(
                name="LoginResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                    "data": inline_serializer(
                        name="LoginData",
                        fields={
                            "access": serializers.CharField(),
                            "refresh": serializers.CharField(),
                            "user": inline_serializer(
                                name="LoginUserData",
                                fields={
                                    "id": serializers.IntegerField(),
                                    "username": serializers.CharField(),
                                    "email": serializers.EmailField(),
                                },
                            ),
                        },
                    ),
                },
            ),
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return BaseResponse.validation_error(serializer.errors)

        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user is None:
            return BaseResponse.error("Invalid username or password.", status_code=401)

        if not user.is_active:
            return BaseResponse.error("This account has been disabled.", status_code=401)

        refresh = RefreshToken.for_user(user)

        return BaseResponse.success(data={
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
        })


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Auth"],
        summary="Refresh access token",
        request=RefreshTokenSerializer,
        responses={
            200: inline_serializer(
                name="RefreshTokenResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                    "data": inline_serializer(
                        name="RefreshTokenData",
                        fields={"access": serializers.CharField()},
                    ),
                },
            ),
        },
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return BaseResponse.bad_request("'refresh' token is required.")

        try:
            refresh = RefreshToken(refresh_token)
            return BaseResponse.success(data={"access": str(refresh.access_token)})
        except TokenError as e:
            return BaseResponse.error(str(e), status_code=401)


class LogoutView(APIView):

    @extend_schema(
        tags=["Auth"],
        summary="Blacklist refresh token (logout)",
        request=LogoutSerializer,
        responses={
            200: inline_serializer(
                name="LogoutResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                },
            ),
        },
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return BaseResponse.bad_request("'refresh' token is required.")

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return BaseResponse.success(message="Successfully logged out.")
        except TokenError as e:
            return BaseResponse.error(str(e), status_code=401)
