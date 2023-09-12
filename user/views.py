from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView)
from rest_framework.response import Response
from .models import Users
from .serializers import (UserRegistrationSerializer, UserLoginSerializer)
from rest_framework.permissions import (AllowAny, IsAuthenticated)


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

