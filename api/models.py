from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models


class ChatRoom(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class ChatMembership(models.Model):
    ROLE_ADMIN = "ADMIN"
    ROLE_MODERATOR = "MODERATOR"
    ROLE_MEMBER = "MEMBER"

    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_MODERATOR, "Moderator"),
        (ROLE_MEMBER, "Member"),
    )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_memberships",
    )
    room = models.ForeignKey(
        "api.ChatRoom",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "room")
        verbose_name = "Chat Membership"
        verbose_name_plural = "Chat Memberships"

    def __str__(self) -> str:
        return f"{self.user} in {self.room} as {self.role}"


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    room = models.ForeignKey(
        "api.ChatRoom",
        on_delete=models.CASCADE,
        related_name="messages",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    content = models.TextField(validators=[MaxLengthValidator(1000)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.author}: {self.content[:30]}"
