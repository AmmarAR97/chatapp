# from channels.db import database_sync_to_async
# from chat_2.models import UserChatRoomDetails, MessageRecord
# from user.models import User
# from django.db.models import Q
# from .serializer import ChatListSerializer, ChatHistorySerializer
# from django.db.models import Count
# from social_dyt.facebook_insta import convert_iso_to_local_time
# from datetime import datetime
#
# @database_sync_to_async
# def user_connection_status(status, user, channel_name=None):
#     """
#     Instance: When user comes online / when websocket connection is established.
#               When user goes offline / when websocket connection is disconnected.
#     Args:
#         user = user instance / id
#         channel_name = unique channel name generated during websocket connection (self.channel_name)
#         status = online / offline
#     """
#     if status == "online":
#         new_values = {
#             'private_channel_name': channel_name,
#             'is_online': True
#         }
#         online_status = UserChatRoomDetails.objects.update_or_create(user_id=int(user), defaults=new_values)
#         MessageRecord.objects.filter(Q(receiver_user_id__id=int(user))|Q(receiver_channel_id__members=int(user))).exclude(sender_id=int(user)).update(is_delivered=True)
#     elif status == "offline":
#         online_status = UserChatRoomDetails.objects.filter(user_id=int(user)).update(is_online=False)
#     else:
#         raise Exception("Invalid input received in status parameter")
#     return online_status
#
#
# @database_sync_to_async
# def get_user_channel_name(user_id):
#     """
#     Instance: returns the channel name if the user is online.
#     """
#     channel_name = UserChatRoomDetails.objects.filter(user=int(user_id)).values("private_channel_name").last().get(
#         "private_channel_name")
#     return channel_name if channel_name else None
#
#
# @database_sync_to_async
# def save_chat(message_data, chat_type):
#
#     sent_by = User.objects.get(pk=int(message_data["sent_by"]))
#     if chat_type == "private":
#         send_to = User.objects.get(pk=int(message_data["send_to"]))
#         personal_chat_thread = DytChannels.objects.filter(channel_type="personal chat", members__in=[sent_by, send_to]).annotate(u_count=Count('members')).filter(u_count=2)
#         if personal_chat_thread.exists():
#             private_group = personal_chat_thread.first()
#         else:
#             private_group = DytChannels.objects.create(title=None)
#             private_group.members.add(sent_by)
#             private_group.members.add(send_to)
#             private_group.save()
#
#         MessageRecord.objects.create(
#             sender=sent_by,
#             receiver_user_id=send_to,
#             receiver_channel_id=private_group,
#             message=message_data["message"],
#             message_content_type='text',
#         )
#     elif chat_type == "group":
#         send_to = DytChannels.objects.get(slug=message_data["send_to"])
#         MessageRecord.objects.create(
#             sender=sent_by,
#             receiver_channel_id=send_to,
#             message=message_data["message"],
#             message_content_type='text',
#         )
#
#
# @database_sync_to_async
# def get_users_chat_list(user_id):
#     """
#     Getting the list of user chat
#     """
#     try:
#         query = MessageRecord.objects.filter(receiver_channel_id__members=user_id)
#         chat_list = query.distinct(
#             "receiver_user_id", "receiver_channel_id"
#         ).values(
#             "sender__id", "receiver_user_id__id", "receiver_user_id__username", "receiver_user_id__avatar",
#             "receiver_channel_id__id", "receiver_channel_id__title", "message", "message_content_type",
#             "is_delivered", "updated_at", 'is_delivered', "is_read"
#         )
#         res = []
#         x = 0
#         for chat in chat_list:
#             data = {
#                 'receiver_name': chat.get('receiver_user_id__username', None),
#                 "is_group_chat": False,
#                 "is_personal_chat": True, "receiver_id": chat.get('receiver_user_id__id', None)}
#             if not data['receiver_name']:
#                 data["is_personal_chat"] = False
#                 data["is_group_chat"] = True
#                 data["receiver_name"] = chat.get('receiver_channel_id__title', None)
#
#             data["message"] = chat.get('message', "")
#             data["timestamp"] = chat.get('updated_at', "Undefined").date().day
#             data["message_type"] = chat.get('message_content_type', None)
#             # sender_name = chat.get('sender__id', None)
#             data["sender_user_id"] = chat.get('sender__id', None)
#             data["is_delivered"] = chat.get('is_delivered', None)
#             data['is_read'] = chat.get('is_read', None)
#             data['receiver_avatar'] = chat.get('receiver_user_id__avatar__url', None)
#             # data['unread_messages_count'] = message_counts[x]
#             data['unread_messages_count'] = MessageRecord.objects.filter(receiver_channel_id=data["receiver_id"], is_read=False).exclude(sender_id=user_id).count()
#             res.append(data)
#             x+=1
#
#
#             # data = {
#             #     "sender": chat.get("sender__id", None),
#             #     # "receiver": chat.get("sender__id", None),
#             #     "receiver_id": chat.get("sender__id", None),
#             #     "message": chat.get("sender__id", None),
#             #     "message_content_type": chat.get("sender__id", None),
#             #     "is_read": chat.get("sender__id", None),
#             #     "is_delivered": chat.get("sender__id", None),
#             #     "created_at": chat.get("sender__id", None),
#             #     "receiver_avatar": chat.get("sender__id", None)
#             # }
#         print(res)
#         # serializer = ChatListSerializer(chat_list, many=True)
#         return {"data": res}
#     except Exception as E:
#         print(E)
#         pass
#
#
# @database_sync_to_async
# def get_users_chat_history(user_id, chat_id, chat_type):
#     """
#     Getting the list of user chat
#     """
#     # todo: we can user group_slug or receiver channel name here to unify receiver
#     try:
#         if chat_type == "private":
#             personal_chat_thread = DytChannels.objects.filter(channel_type="personal chat",
#                                                               members__id__in=[user_id, chat_id]).annotate(
#                 u_count=Count('members')).filter(u_count=2)
#             chat_history = MessageRecord.objects.filter(
#                 receiver_channel_id=personal_chat_thread.first()
#             )
#             chat_history.update(is_read=True)  # .order_by('-id')[:30]
#         elif chat_type == "group":
#             chat_history = MessageRecord.objects.filter(
#                 receiver_channel_id__slug=chat_id
#             )
#             chat_history.update(is_read=True)#.order_by('-id')[:30]
#         else:
#             pass
#         # serializer = ChatHistorySerializer(chat_history, many=True)
#         chat_list = chat_history.order_by('-id')[:30].values(
#             "sender__id", "receiver_user_id__id", "receiver_user_id__username", "receiver_user_id__avatar",
#             "receiver_channel_id__id", "receiver_channel_id__title", "message", "message_content_type",
#             "is_delivered", "updated_at", 'is_delivered', "is_read"
#
#             # "updated_at", "is_read", 'receiver_user_id__avatar__url'
#         )#.annotate(Count("is_delivered"), Count("is_read"))
#         res = []
#         for chat in chat_list:
#             # for chat in query:
#
#             data = {}
#             data["receiver_id"] = chat.get('receiver_user_id__id', None)
#             data["is_group_chat"] = False
#             data["is_personal_chat"] = True
#             if not data["receiver_id"]:
#                 data["is_group_chat"] = True
#                 data["is_personal_chat"] = False
#             data["sender_user_id"] = chat.get('sender__id', None)
#             data["message"] = chat.get('message', "")
#             data["timestamp"] = chat.get('updated_at', "Undefined").date().day
#             data["message_type"] = chat.get('message_content_type', None)
#             # sender_name = chat.get('sender__id', None)
#
#             data["is_delivered"] = chat.get('is_delivered', None)
#             data['is_read'] = chat.get('is_read', None)
#
#             res.append(data)
#             # unread_messages_count = chat.get('receiver_user_id__id', None)
#
#             # data = {
#             #     "sender": chat.get("sender__id", None),
#             #     # "receiver": chat.get("sender__id", None),
#             #     "receiver_id": chat.get("sender__id", None),
#             #     "message": chat.get("sender__id", None),
#             #     "message_content_type": chat.get("sender__id", None),
#             #     "is_read": chat.get("sender__id", None),
#             #     "is_delivered": chat.get("sender__id", None),
#             #     "created_at": chat.get("sender__id", None),
#             #     "receiver_avatar": chat.get("sender__id", None)
#             # }
#         return res
#     except Exception as E:
#         print(E)
#
#
# @database_sync_to_async
# def get_users_chat_profile(chat_id, chat_type):
#     """
#     Getting the list of user chat
#     """
#     try:
#         if chat_type == "private":
#             user = User.objects.get(pk=chat_id)
#             # try:
#             #     receiver_avatar = user.avatar.url
#             # except Exception as E:
#             #     receiver_avatar = "https://irelandprodbucket.s3.amazonaws.com/media/avatars/default_user_avatar.png"
#             #
#             # data = {"receiver_avatar": receiver_avatar, "receiver_name": user.username}
#             data = {}
#
#             user_status = UserChatRoomDetails.objects.get(user=user)
#             data["online"] = user_status.is_online
#             data["last_seen"] = "online" if data["online"] else user_status.updated_at.strftime("%D")
#
#             # data["last_seen"] = "online" if data["online"] else user_status.updated_at == datetime.today()
#             # user_status.updated_at.strftime("%D")
#
#             return data
#
#         elif chat_type == "group":
#             group = DytChannels.objects.get(slug=chat_id)
#             try:
#                 receiver_avatar = group.receiver_channel_id.icon.url
#             except Exception as E:
#                 receiver_avatar = "https://irelandprodbucket.s3.amazonaws.com/media/avatars/default_user_avatar.png"
#             return {"receiver_avatar": receiver_avatar, "receiver_name": group.title}
#         else:
#             pass
#     except Exception as E:
#         print(E)
#
#
# # def create_personal_chat_channel(user_one_user_id, user_two_user_id):
# #     """
# #     Making this to avoid long query over messages.
# #
# #     if int(user_one_user_id) > int(user_two_user_id):
# #         title = {user_two_user_id}_{user_one_user_id}
# #     else:
# #         title = {user_one_user_id}_{user_two_user_id}
# #     """
# #     if int(user_one_user_id) > int(user_two_user_id):
# #         title = f"{user_two_user_id}_{user_one_user_id}"
# #     else:
# #         title = f"{user_one_user_id}_{user_two_user_id}"
# #
# #     private_group = DytChannels.objects.create(title=title)
# #
# #     user1 = User.objects.get(pk=int(user_one_user_id))
# #     user2 = User.objects.get(pk=int(user_two_user_id))
# #     private_group.members.add(user1)
# #     private_group.members.add(user2)
# #     private_group.save()
#
#
# """
# Types of chat:
#
# personal chat --> will be seen if there is chat history.
# group chat --> will be seen regardless of the chat history.
#  x = MessageRecord.objects.filter(Q(sender=63647)|Q(receiver_user_id=63646)|Q(receiver_channel_id__members=63647)).order_by("receiver_user_id", "receiver_channel_id","-updated_at").distinct("receiver_user_id", "receiver_channel_id")
#
# """
