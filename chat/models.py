from user.models import Users
from django.db import models


class ChatBaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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

