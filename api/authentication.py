from datetime import datetime, timezone

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            raise exceptions.AuthenticationFailed("Invalid Authorization header format. Expected 'Bearer <token>'.")

        token = parts[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token.")

        user_id = payload.get("user_id")
        username = payload.get("username")
        if not user_id or not username:
            raise exceptions.AuthenticationFailed("Invalid token payload.")

        User = get_user_model()
        try:
            user = User.objects.get(id=user_id, username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found.")

        return (user, token)
