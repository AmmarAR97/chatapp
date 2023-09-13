from django.urls import path
from .views import OnlineUsersView
# http://127.0.0.1:8000/api/v1/chat_2/ammar
urlpatterns = [
    path("api/online-users/", OnlineUsersView.as_view(), name="fetch_online_users"),
    # path("api/chat/start/<int:user_id>/", PersonalChatView.as_view(), name="private-chat"),
]

