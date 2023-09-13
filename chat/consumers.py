import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import MessageRecord


# class ChatConsumer(AsyncWebsocketConsumer):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#         self.user_id = None
#         self.username = None
#
#     async def connect(self):
#         """
#         Authenticate the user and allow the connection
#         """
#         # if self.scope["user"].is_authenticated:
#         print("Im at connect")
#         if self.scope["user"]:
#             await self.accept()
#             self.user_id = self.scope["user"].id
#             self.username = self.scope["user"].username
#         else:
#             await self.close()
#
#     async def disconnect(self, close_code):
#         pass  # Handle WebSocket disconnect
#
#     async def receive(self, text_data=None, bytes_data=None):
#         # Handle incoming WebSocket messages
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         receiver_user_id = text_data_json["receiver_user_id"]
#
#         # Check if the receiver is online
#         receiver_user = await self.get_user(receiver_user_id)
#         if receiver_user and receiver_user.profile.online:
#             # receiver is online, send the message
#             await self.send_message(receiver_user.username, message)
#         else:
#             # receiver is offline, handle accordingly (e.g., store in the database)
#             # await self.handle_offline_message(receiver_username, message)
#             pass
#
#     async def send_message(self, receiver_username, message):
#         # Send the message to the receiver
#         await self.send(text_data=json.dumps({
#             "message": message,
#             "from": self.username,
#         }))
#
#     @database_sync_to_async
#     def get_user(self, username):
#         try:
#             return User.objects.get(username=username)
#         except User.DoesNotExist:
#             return None
#
#     @database_sync_to_async
#     def handle_offline_message(self, receiver_username, message):
#         # Store the offline message in the database or handle it as needed
#         sender_user = User.objects.get(username=self.username)
#         receiver_user = User.objects.get(username=receiver_username)
#         MessageRecord.objects.create(author=sender_user, receiver=receiver_user, content=message)


import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
# from .helper_functions import (
#     user_connection_status, get_user_channel_name, save_chat, community_manager,groups_user_is_part_of,
#     get_users_chat_list, get_users_chat_history, get_users_chat_profile
# )
from asgiref.sync import async_to_sync
from django.core.serializers.json import DjangoJSONEncoder


class PersonalChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_room = None
        self.receiver = None
        self.room_name = None
        self.user_id = None
        self.user_name = None
        self.count = 0

    async def connect(self):
        self.user_name = self.scope['url_route']['kwargs']['username']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        channel_name = self.channel_name

        await self.accept()
        # await user_connection_status(status="online", user=self.user_id, channel_name=channel_name)

    async def disconnect(self, close_code):
        pass
        # Note that in some rare cases (power loss, etc) disconnect may fail
        # to run; this naive example would leave zombie channel names around.
        # await user_connection_status(status="offline", user=self.user_id)

    # Receive message from WebSocket
    async def receive(self, text_data):
        """
        sample body:

        user 1 = {"message": "I'm user 1",
        "sender": "ahmed",
        "chat_type": "private",
        "send_to": "63646"}

        user 2 = {"message": "I'm user 2",
        "sender": "ammar",
        "chat_type": "private",
        "send_to": "63647"}

        """
        text_data_json = json.loads(text_data)

        # message --> message to send
        # chat_type --> group / private

        message = text_data_json['message']
        receiver_user_id = text_data_json['send_to']

        send_to = None  # --> user_id / group_name
        if text_data_json['chat_type'] == "private":
            pass
            # send_to = await get_user_channel_name(user_id=text_data_json['send_to'])

        # elif text_data_json['chat_type'] == "group": # Todo : Discuss with Deepak
        #     send_to = text_data_json['send_to']

        if send_to:  # If user is online send over websocket
            await self.channel_layer.send(
                send_to, {
                    'type': 'chatroom.message',
                    'message': message,
                    'username': self.user_name,
                    'receiver_user_id': receiver_user_id,
                    'chat_type': text_data_json['chat_type'],
                    'sent_by': self.user_id
                }
            )
        else:  # Else save message to DB
            pass
            # await save_chat(
            #     {
            #         "sender": self.user_id,
            #         "receiver_user_id": receiver_user_id,
            #         "message": message,
            #         'chat_type': text_data_json['chat_type']
            #     },
            #     text_data_json['chat_type']
            # )

    # Receive message from channel_name
    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']
        receiver_user_id = event['receiver_user_id']
        chat_type = event['chat_type']
        sent_by = event['sent_by']

        # Sends message over websocket
        await self.send(
            text_data=json.dumps(
                {
                    'message': message,
                    'username': username,
                }
            )
        )

        # Saving message to DB
        # await save_chat(
        #     {
        #         "sender": sent_by,
        #         "receiver_user_id": receiver_user_id,
        #         "message": message,
        #         'chat_type': chat_type
        #     },
        #     chat_type
        # )

    async def update_user_last_activity(self):
        if self.scope["user"].is_authenticated:
            pass
            # user_profile = UserProfile.objects.get(user=self.scope["user"])
            # user_profile.last_activity = timezone.now()
            # user_profile.save()
