from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'contact_number', 'gender', 'birth_date']


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Check if either username or email is provided
        if not (username or email):
            raise serializers.ValidationError("Either username or email is required.")

        # Check if the user is authenticated based on provided username/email and password
        user = authenticate(username=username, email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials.")

        data['user'] = user
        return data
