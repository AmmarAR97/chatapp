from rest_framework import serializers
from .models import Users


class OnlineUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'gender', 'private_channel_name']
