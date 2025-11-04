from typing import Tuple

from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .authentication import JWTAuthentication
from .jwt_utils import generate_jwt
from .models import ChatMembership, ChatRoom, Message
from .permissions import IsAuthenticatedJWT, IsMessageOwnerOrModerator
from .serializers import (
    ChatRoomSerializer,
    LoginSerializer,
    MessageCreateSerializer,
    MessageSerializer,
    RegisterSerializer,
    UserPublicSerializer,
)


User = get_user_model()


def get_default_room() -> ChatRoom:
    room, _ = ChatRoom.objects.get_or_create(name='Общий')
    return room


def ensure_membership(user: User) -> ChatMembership:
    room = get_default_room()
    membership, _ = ChatMembership.objects.get_or_create(user=user, room=room, defaults={"role": ChatMembership.ROLE_MEMBER})
    return membership


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = User.objects.create_user(username=username, password=password)
        membership = ensure_membership(user)
        token = generate_jwt(user)
        return Response(
            {
                "token": token,
                "user": UserPublicSerializer(user).data,
                "role": membership.role,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        membership = ensure_membership(user)
        token = generate_jwt(user)
        return Response(
            {
                "token": token,
                "user": UserPublicSerializer(user).data,
                "role": membership.role,
            }
        )


class MeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedJWT]

    def get(self, request):
        membership = ensure_membership(request.user)
        return Response(
            {
                "id": request.user.id,
                "username": request.user.username,
                "role": membership.role,
            }
        )


class MessagesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedJWT]

    def get(self, request):
        # Ensure default room and membership
        ensure_membership(request.user)
        room = get_default_room()
        try:
            limit = int(request.query_params.get("limit", 50))
        except ValueError:
            limit = 50
        try:
            offset = int(request.query_params.get("offset", 0))
        except ValueError:
            offset = 0
        limit = max(1, min(limit, 200))
        offset = max(0, offset)

        qs = Message.objects.filter(room=room).select_related("author").order_by("created_at")
        count = qs.count()
        results = qs[offset : offset + limit]
        data = MessageSerializer(results, many=True, context={"request": request}).data
        return Response({"count": count, "results": data})

    def post(self, request):
        ensure_membership(request.user)
        serializer = MessageCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        out = MessageSerializer(message, context={"request": request}).data
        return Response(out, status=status.HTTP_201_CREATED)


class MessageDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedJWT, IsMessageOwnerOrModerator]

    def delete(self, request, id: int):
        room = get_default_room()
        message = get_object_or_404(Message.objects.select_related("author", "room"), id=id, room=room)
        # Object-level permission check
        self.check_object_permissions(request, message)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedJWT]

    def get(self, request):
        room = get_default_room()
        ensure_membership(request.user)
        return Response(ChatRoomSerializer(room).data)
