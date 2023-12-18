# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView
)
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, Token


from apps.accounts.api.v1.serializers.login import LoginSerializer
from apps.accounts.selectors.user_selector import UserSelector
from apps.accounts.services.session import SessionService
from apps.accounts.api.v1.serializers.login import (
    TokenVerifyResponseSerializer, CustomTokenObtainPairSerializer
)

from apps.accounts.api.v1.serializers.session import (
    GoogleTokenSerializer,
    SessionSerializer,
    AccessTokenSerializer,
)
from apps.accounts.api.v1.serializers.user_profile import (
    UserProfileSerializer,
)
from apps.accounts.models import User


class GoogleLoginView(APIView):
    """Process a google token_id login."""

    def post(self, request):
        """Get session from google token id.

        POST /api/v1/auth/google-login/
        """
        serializer = GoogleTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = SessionService.process_google_token(
            serializer.validated_data['token'],
        )

        return Response(SessionSerializer(user).data)


class FacebookLoginView(APIView):
    def post(self, request):
        """Get session from facebook access token.

        POST /api/v1/auth/facebook-login/
        """
        serializer = AccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = SessionService.process_facebook_token(
            serializer.validated_data['access_token']
        )

        return Response(SessionSerializer(user).data)


class LoginView(APIView):
    """Process a google token_id login."""

    def post(self, request):
        """Get session from google token id.

        POST /api/v1/auth/login/
        """
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        username_or_email = serializer.validated_data.get('user')
        plain_password = serializer.validated_data.get('password')

        user = UserSelector.get_by_username_or_email(username_or_email)
        SessionService.validate_session(user, plain_password)

        return Response(SessionSerializer(user).data)


class TokenVerifyAPIView(TokenVerifyView):
    serializer_class = TokenVerifyResponseSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("\n\n headers: ", request.headers)
        authorization = request.headers.get('Authorization', None)
        if (authorization is not None):
            _token = request.headers['Authorization']
            token = _token.split()[1]
        else:
            token = request.data.get('token')

        print("\n\n token: ", token)

        if token is None:
            return Response({'error': 'Token is missing.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)

            return Response(SessionSerializer(user).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
