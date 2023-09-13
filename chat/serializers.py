from rest_framework import serializers
from .models import Users


class OnlineUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'contact_number', 'gender', 'birth_date']
