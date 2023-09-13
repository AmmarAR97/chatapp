from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView, UpdateAPIView)
from rest_framework.response import Response
from .models import Users
from .serializers import (UserRegistrationSerializer, UserLoginSerializer, UserUpdateSerializer)
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.authtoken.views import ObtainAuthToken


class UserRegistrationView(CreateAPIView):
    """
    View for user registration.

    This view allows users to register by providing their username, email, and password.
    Upon successful registration, a user account is created, and a success message is returned.

    Request:
    - POST data: {'username': 'user1', 'email': 'user1@neofi.com', 'password': 'password'}
    - POST data optional fields = ['first_name', 'last_name', 'contact_number', 'gender', 'birth_date']

    Response (successful registration):
    - Status Code: 201 (Created)
    - Response Data:
        {
            'message': 'User registration successful',
            'user_data': {
                'id': 1,
                'username': 'user1',
                'email': 'user1@neofi.com',
                'contact_number': null,
                'gender': null,
                'birth_date': null
            }
        }
    """

    permission_classes = [AllowAny]
    queryset = Users.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = {
            'message': 'User registration successful',
            'user_data': serializer.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class UserLoginView(GenericAPIView):
    """
    View for user login.

    This view allows users to log in by providing their username/email and password.
    Upon successful login, an authentication token is generated and returned.

    Request:
    - POST data: {'username': 'user1', 'password': 'password'}
    - POST data optional: {'email': 'user1@neofi.com', 'username': 'user1', 'password': 'password'}

    Response (successful login):
    - Status Code: 200 (OK)
    - Response Data:
        {
            'message': 'Login successful',
            'token': 'your-auth-token-string'
        }
    """

    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create or retrieve an authentication token for the user
        access_token = serializer.validated_data.get('access_token')

        if access_token:
            return Response(
                {'message': 'Login successful', 'access_token': access_token},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Login failed or something went wrong!', 'access_token': None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
from django.contrib.auth.mixins import LoginRequiredMixin

class UserUpdateView(LoginRequiredMixin, UpdateAPIView):
    """
    View for updating user details.

    This view allows authenticated users to update their user details.

    Request (authenticated user):
    - PATCH data: {
        'first_name': 'NewFirstName',
        'last_name': 'NewLastName',
        'contact_number': 'NewContactNumber',
        'gender': 'new_gender',
        'birth_date': 'new_birth_date'
      }

    Response (successful update):
    - Status Code: 200 (OK)
    - Response Data: {'message': 'User data updated successfully', 'data': Updated user details}

    Response (failed update):
    - Status Code: 400 (Bad Request)
    - Response Data: Validation errors
    """
    queryset = Users.objects.all()
    serializer_class = UserUpdateSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'User data updated successfully', 'data': serializer.data},
            status=status.HTTP_200_OK
        )
