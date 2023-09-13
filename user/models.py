from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class Users(AbstractUser):
    gender = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    contact_number = models.PositiveBigIntegerField(db_index=True, unique=True, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=gender, blank=True, null=True)
    # Todo: add profile pic if needed
    birth_date = models.DateField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    private_channel_name = models.CharField(max_length=35, null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_tokens_for_user(self):
        refresh = RefreshToken.for_user(self)
        return f"{str(refresh.access_token)}"

    def __str__(self):
        return self.username


class ReportedUsers(models.Model):

    ACTION_CHOICES = (
        ('block', 'Block'),
        ('report', 'Report'),
    )

    reporter = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='blocking_users')
    target_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='blocked_users')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    reason = models.TextField(blank=True)
    attachments = models.FileField(upload_to='media/reported/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.action == "block":
            return f'{self.reporter.username} blocked {self.target_user.username}'
        else:
            return f'{self.reporter.username} reported {self.target_user.username}'

