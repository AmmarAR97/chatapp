from django.urls import path
from .views import OnlineUsersView, StartChatView


urlpatterns = [
    path("api/online-users/", OnlineUsersView.as_view(), name="fetch_online_users"),
    path("api/chat/start/<int:pk>/", StartChatView.as_view(), name="start-chat"),
]

