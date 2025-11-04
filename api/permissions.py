from rest_framework.permissions import BasePermission

from .models import ChatMembership, ChatRoom


def get_default_room():
    room, _ = ChatRoom.objects.get_or_create(name='Общий')
    return room


class IsAuthenticatedJWT(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsMessageOwnerOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj is expected to be a Message instance
        if not request.user or not request.user.is_authenticated:
            return False
        if getattr(obj, "author_id", None) == getattr(request.user, "id", None):
            return True
        room = get_default_room()
        membership = ChatMembership.objects.filter(user=request.user, room=room).first()
        if not membership:
            return False
        return membership.role in (ChatMembership.ROLE_ADMIN, ChatMembership.ROLE_MODERATOR)
