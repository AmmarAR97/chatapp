from rest_framework import status
from rest_framework.generics import (ListAPIView, GenericAPIView)
from rest_framework.response import Response
from user.models import Users
from .serializers import OnlineUsersSerializer
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer


class OnlineUsersView(ListAPIView):
    """
    View for retrieving a list of online users.

    This view requires user authentication and returns a list of users
    who have the 'is_online' attribute set to True.

    Returns:
        HTTP Response: A JSON response containing the list of online users.

    Example:
        To fetch the list of online users, make a GET request to the endpoint 'api/users/online/'.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = OnlineUsersSerializer

    def get_queryset(self):
        return Users.objects.filter(is_online=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            'message': 'Online users fetched successfully',
            'data': serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class StartChatView(GenericAPIView):
    """
    View for initiating a chat with a user, upgrading to WebSocket if the user is online.

    This view requires user authentication and allows a user to start a chat session with another user.
    If the target user is online, the request is upgraded to WebSocket for real-time chat.

    Returns:
        HTTP Response: A JSON response indicating the status of the chat initiation.

    Example:
        To initiate a chat with a user, make a POST request to the endpoint 'api/chat/start/' with the target user's details.
    """

    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_online:
            # Send message via live channels channels
            channel_layer = get_channel_layer()
            channel_layer.send(
                user.private_channel_name,
                {
                    'type': 'chatroom.message',
                    'message': 'message',
                    'username': 'self.user_name',
                    'receiver_user_id': 'receiver_user_id',
                    'chat_type': 'private',
                    'sent_by': 'self.user_id'
                }
            )
            return Response({'message': 'Message sent!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User is not online'}, status=status.HTTP_400_BAD_REQUEST)
