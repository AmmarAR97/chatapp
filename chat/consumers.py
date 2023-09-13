import json
from channels.generic.websocket import AsyncWebsocketConsumer
from user.models import Users
from channels.db import database_sync_to_async
from .models import MessageRecord


@database_sync_to_async
def save_user_channel_name(user_id, channel_name):
    try:
        user = Users.objects.get(pk=user_id)
        user.private_channel_name = channel_name
        user.save()
        return True
    except Exception as E:
        print(E)
        return


@database_sync_to_async
def get_user_channel_name(user_id):
    try:
        return Users.objects.get(pk=user_id).private_channel_name
    except Exception as E:
        print(E)
        return


@database_sync_to_async
def set_user_offline(user_id):
    try:
        user = Users.objects.get(pk=user_id)
        user.is_online = False
        user.private_channel_name = None
        user.save()
    except Exception as E:
        print(E)


@database_sync_to_async
def save_chat(message_obj):

    users = Users.objects.filter(pk__in=[message_obj['sender_id'], message_obj['receiver_user_id']])

    if users[0].id == message_obj['sender_id']:
        sender = users[0]
        receiver = users[1]
    else:
        sender = users[1]
        receiver = users[0]

    # Create a MessageRecord instance and set its attributes
    message_record = MessageRecord(
        author=sender,
        receiver=receiver,
        message=message_obj['message'],
        is_read=False,  # We can work on this while FE integrates BE
        message_content_type="text",  # We can work on this while FE integrates BE
        media_file=None,  # We can work on this while FE integrates BE
        is_delivered=False, # We can work on this while FE integrates BE
        is_deleted=False,  # We can work on this while FE integrates BE
    )

    # Save the message record to the database
    message_record.save()
    pass


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
                    'chat_type': text_data_json['chat_type'],
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
