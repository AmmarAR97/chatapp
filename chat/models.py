from user.models import Users
from django.db import models


class ChatBaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserChatRoomDetails(models.Model):
    """
    Saving Channel name when the user is live!
    """
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_chat_room')
    private_channel_name = models.CharField(max_length=35, null=True, blank=True)
    is_online = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True) # last seen

    def __str__(self) -> str:
        return f'<{self.user}>'


# class Connection(ChatBaseModel):
#
#     user1 = models.ForeignKey(Users, on_delete=models.CASCADE)
#     user2 = models.ForeignKey(Users, on_delete=models.CASCADE)
#     is_active = models.BooleanField(default=True)
#     is_blocked_by_user1 = models.BooleanField(default=False)
#     reported_by_user1 = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'Connection between {self.user1.username} and {self.user2.username}'


class MessageRecord(ChatBaseModel):

    TYPE_OF_CONTENT = (
        ("text", "Text"),
        ("image", "Image"),
        ("docs", "Docs"),
        ("video", "Video"),
        ("audio", "Audio"),
    )
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="message_author")
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="message_receiver")
    # connections = models.ForeignKey(Connection, on_delete=models.CASCADE)
    message = models.TextField(blank=False, null=False)
    is_read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        "self", on_delete=models.CASCADE, limit_choices_to={'parent_message': None}, null=True, blank=True
    )
    message_content_type = models.CharField(max_length=10, choices=TYPE_OF_CONTENT, default="text")
    media_file = models.FileField(upload_to='media/messages/')
    is_delivered = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Sent By: {self.author.username} - Received By: {self.receiver.username}'

    class Meta:
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['receiver']),
            models.Index(fields=['created_at']),
        ]


# class ThreadManager(models.Manager):
#     def get_or_create_personal_thread(self, user1, user2):
#         threads = self.get_queryset().filter(thread_type='personal')
#         threads = threads.filter(users__in=[user1, user2]).distinct()
#         threads = threads.annotate(u_count=Count('users')).filter(u_count=2)
#         if threads.exists():
#             return threads.first()
#         else:
#             thread = self.create(thread_type='personal')
#             thread.users.add(user1)
#             thread.users.add(user2)
#             return thread
#
#     def by_user(self, user):
#         return self.get_queryset().filter(users__in=[user])


# class Thread(ChatBaseModel):
#     THREAD_TYPE = (
#         ('personal', 'Personal'),
#         # ('group', 'Group')
#     )
#
#     name = models.CharField(max_length=50, null=True, blank=True)
#     thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='personal')
#     users = models.ManyToManyField(Users)
#
#     objects = ThreadManager()
#
#     def __str__(self) -> str:
#         # if self.thread_type == 'personal' and self.users.count() == 2:
#         return f'{self.users.first()} and {self.users.last()}'
#         # return f'{self.name}'


# class Message(ChatBaseModel):
#     thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
#     sender = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sender')
#     receiver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='receiver')
#     text = models.TextField(blank=False, null=False)
#
#     def __str__(self) -> str:
#         return f'From <Thread - {self.thread}>'


# class UserChatRoomDetails(ChatBaseModel):
#     """
#     Saving Channel name when the user is live!
#     """
#     user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user')
#     private_channel_name = models.CharField(max_length=35, null=True, blank=True)
#     is_online = models.BooleanField(default=False)
#     updated_at = models.DateTimeField(auto_now=True) # last seen
#
#     def __str__(self) -> str:
#         return f'<{self.user}>'
#
#
# class DytChannels(models.Model):
#     """
#     Note:
#          for private channel title maintain the following logic to keep it unique
#
#          if int(user_one_user_id) > int(user_two_user_id):
#
#                 title = {user_two_user_id}_{user_one_user_id}
#          else:
#                 title = {user_one_user_id}_{user_two_user_id}
#     """
#     CHANNEL_TYPE = (
#         ('closed community', 'Closed Community'),
#         ('open community', 'Open Community'),
#         ('broadcast', 'Broadcast'),
#         ('personal chat', 'Personal Chat')
#     )
#     channel_type = models.CharField(max_length=16, choices=CHANNEL_TYPE, default='personal chat')
#     title = models.CharField(max_length=30, null=True, blank=True)
#     slug = models.SlugField(blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_admin', null=True, blank=True)
#     members = models.ManyToManyField(User, related_name='group_participants')
#     description = models.CharField(max_length=500, null=False, blank=False)
#     icon = models.FileField(null=True, blank=True, upload_to=dyt_channel_profile_pic_path)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self) -> str:
#         return f'{self.title} - {self.channel_type}'
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = unique_slug_generator(self, self.title)
#         super(DytChannels, self).save(*args, **kwargs)

