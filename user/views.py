from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView, UpdateAPIView, RetrieveAPIView)
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Users
from .serializers import (UserRegistrationSerializer, UserLoginSerializer, UserUpdateSerializer)
from rest_framework.permissions import (AllowAny, IsAuthenticated)
import json
from .helper import calculate_similarity


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

    Note:
        After a successful login, the frontend is expected to upgrade the connection to a WebSocket to enable the
        user to receive real-time live messages.
        use: ws/chat/go-live/user_id/
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


class UserUpdateView(UpdateAPIView):
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
    permission_classes = [IsAuthenticated]

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


class UserLogoutView(APIView):
    """
    A view for handling user logout by setting the 'is_online' flag to False.

    This view requires user authentication, and upon successful logout,
    it updates the 'is_online' attribute of the authenticated user to False.

    Returns:
        HTTP Response: A JSON response indicating the logout status.

    Example:
        To log out the currently authenticated user, make a POST request to the endpoint '/user/logout/'.

    Note:
        After successful logout, the frontend is expected to remove the user access token from local storage.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_obj = request.user
        if user_obj:
            user_obj.is_online = False
            user_obj.save()
            return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


class SuggestedFriendsView(RetrieveAPIView):
    """
    A view for retrieving the top 5 suggested friends for a given user based on interests.

    This view allows any user to access it.

    Parameters:
        user_id (int): The ID of the target user for whom suggestions are generated.

    Returns:
        HTTP Response: A JSON response containing the top 5 recommended friends for the
        target user based on similarity of interests.

    Example:
        To retrieve suggested friends for User 145, make a GET request to the endpoint
        'api/suggested-friends/145/'.

    Note:
        The view uses a similarity score based on interests to recommend friends.
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        user_id = kwargs['user_id']

        with open('users.json', 'r') as file:
            data = json.load(file)

        suggested_friends = []

        target_user = data["users"][user_id-1]
        target_interests = set(target_user["interests"])

        for user in data["users"]:
            if user != target_user:
                user_interests = set(user["interests"])
                if user_interests >= target_interests or user_interests <= target_interests:
                    similarity_score = calculate_similarity(target_user, user)
                    suggested_friends.append({"user": user, "similarity": similarity_score})

        # Sort the suggested friends by similarity score in ascending order
        suggested_friends.sort(key=lambda x: x["similarity"], reverse=True)

        return Response(
            {"message": 'Found recommendations!', "recommended_friends": suggested_friends[:5]},
            status=status.HTTP_200_OK
        )
