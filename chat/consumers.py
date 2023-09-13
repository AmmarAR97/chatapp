import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .consumers_helper import (save_user_channel_name, set_user_offline, get_user_channel_name, save_chat)


class PersonalChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_id = None

    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        await self.accept()
        await save_user_channel_name(user_id=self.user_id, channel_name=self.channel_name)

    async def disconnect(self, close_code):
        # Note that in some rare cases (power loss, etc) disconnect may fail
        # to run; this naive example would leave zombie channel names around.
        await set_user_offline(self.user_id)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        """
        sample body:

        user 1 = {
        "message": "I'm user 1",
        "sender": "ahmed",
        "send_to": "1"
        }

        user 2 = {
        "message": "I'm user 2",
        "sender": "ammar",
        "send_to": "2"
        }

        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']  # message --> message to send
        receiver_user_id = text_data_json['send_to']

        send_to = await get_user_channel_name(user_id=text_data_json['send_to'])

        if send_to:  # If user is online send over websocket
            await self.channel_layer.send(
                send_to, {
                    'type': 'chatroom.message',
                    'message': message,
                    'receiver_user_id': receiver_user_id,
                    'sender_id': self.user_id
                }
            )
        else:
            print("Somthing went wrong at consumer receive method!")

    # Receive message from channel_name
    async def chatroom_message(self, event):

        # Sends message over websocket
        await self.send(
            text_data=json.dumps(
                {
                    'message': event['message'],
                    'sender_id': event['sender_id'],
                    # we can add more things here
                }
            )
        )

        # Saving message to DB
        await save_chat(event)
