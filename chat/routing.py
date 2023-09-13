from django.urls import re_path
from .consumers import PersonalChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/go-live/(?P<user_id>\w+)/$', PersonalChatConsumer.as_asgi()),
    re_path(r'ws/chat/send/(?P<user_id>\w+)/$', PersonalChatConsumer.as_asgi()),
]
