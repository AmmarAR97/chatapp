from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    gender = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    contact_number = models.PositiveBigIntegerField(db_index=True, unique=True, default=0)
    gender = models.CharField(max_length=20, choices=gender, blank=True, null=True)
    # Todo: add profile pic if needed
    birth_date = models.DateField(blank=True, null=True)
    online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    # Define related_name for groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='custom_user_model'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='custom_user_model'
    )
