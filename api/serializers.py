from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ChatMembership, ChatRoom, Message


User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ("id", "name")


class MembershipSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source="user_id")
    room = serializers.IntegerField(source="room_id")

    class Meta:
        model = ChatMembership
        fields = ("user", "room", "role")


class MessageSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    can_delete = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ("id", "author", "content", "created_at", "can_delete")
        read_only_fields = ("id", "author", "created_at", "can_delete")

    def get_can_delete(self, obj):
        request = self.context.get("request")
        if not request or not request.user or not request.user.is_authenticated:
            return False
        if obj.author_id == request.user.id:
            return True
        room, _ = ChatRoom.objects.get_or_create(name='Общий')
        membership = ChatMembership.objects.filter(user=request.user, room=room).first()
        if not membership:
            return False
        return membership.role in (ChatMembership.ROLE_ADMIN, ChatMembership.ROLE_MODERATOR)


class MessageCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=1000)

    class Meta:
        model = Message
        fields = ("content",)

    def validate_content(self, value: str) -> str:
        if not isinstance(value, str):
            raise serializers.ValidationError("Content must be a string.")
        cleaned = value.strip()
        if not cleaned:
            raise serializers.ValidationError("Content cannot be empty.")
        if len(cleaned) > 1000:
            raise serializers.ValidationError("Content is too long (max 1000 chars).")
        return cleaned

    def create(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Authentication required")
        room, _ = ChatRoom.objects.get_or_create(name='Общий')
        message = Message.objects.create(
            room=room,
            author=user,
            content=validated_data["content"],
        )
        return message
