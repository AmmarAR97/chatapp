from rest_framework import serializers
from .models import Users
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'contact_number', 'gender', 'birth_date']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        user = Users.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            contact_number=validated_data.get('contact_number'),
            gender=validated_data.get('gender'),
            birth_date=validated_data.get('birth_date')
        )
        return user


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
            # raise serializers.ValidationError("Either username or email is required.")
            raise serializers.ValidationError(
                {'message': 'Either username or email is required.', 'access_token': None}
            )

        # Check if the user is authenticated based on provided username/email and password
        if username and email:
            user = authenticate(username=username, email=email, password=password)
        elif username:
            user = authenticate(username=username, password=password)
        elif email:
            user = authenticate(email=email, password=password)
        else:
            user = None

        if user is None:
            # raise serializers.ValidationError("Invalid credentials.")
            raise serializers.ValidationError({'message': 'Invalid credentials.', 'access_token': None})

        data['access_token'] = user.get_tokens_for_user()
        return data
