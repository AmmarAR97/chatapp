from rest_framework import status
from rest_framework.generics import (ListAPIView, GenericAPIView)
from rest_framework.response import Response
from user.models import Users
from .serializers import OnlineUsersSerializer
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer


class OnlineUsersView(ListAPIView):

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

    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()

    def post(self, request, *args, **kwargs):
        user = self.get_object()

        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_online:
            # Upgrade the request to WebSocket API
            channel_layer = get_channel_layer()
            room_name = f"user_"
            channel_layer.group_add(room_name, self.channel_name)
            return Response({'message': 'WebSocket connection initiated'}, status=status.HTTP_101_SWITCHING_PROTOCOLS)
        else:
            return Response({'error': 'User is not online'}, status=status.HTTP_400_BAD_REQUEST)
