from django.contrib import admin
from .models import ChatRoom, ChatMembership, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)


@admin.register(ChatMembership)
class ChatMembershipAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "room", "role", "created_at")
    list_filter = ("role", "room")
    search_fields = ("user__username", "room__name")
    readonly_fields = ("created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "author", "short_content", "created_at", "updated_at")
    list_filter = ("room", "author")
    search_fields = ("author__username", "content")
    readonly_fields = ("created_at", "updated_at")

    def short_content(self, obj):
        return (obj.content or "")[:50]

    short_content.short_description = "Content"
