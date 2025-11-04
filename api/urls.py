from django.urls import path

from .views import (
    LoginView,
    MeView,
    MessageDeleteView,
    MessagesView,
    RegisterView,
    RoomView,
)

urlpatterns = [
    # Auth
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    # Chat
    path("chat/messages/", MessagesView.as_view(), name="chat-messages"),
    path("chat/messages/<int:id>/", MessageDeleteView.as_view(), name="chat-message-delete"),
    path("chat/room/", RoomView.as_view(), name="chat-room"),
]
