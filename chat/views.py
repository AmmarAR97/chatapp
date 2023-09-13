from rest_framework import status
from rest_framework.generics import (ListAPIView, GenericAPIView, UpdateAPIView)
# from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import Users
from .serializers import OnlineUsersSerializer
from rest_framework.permissions import (AllowAny, IsAuthenticated)


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


# class UserLoginView(GenericAPIView):
#     """
#     View for user login.
#
#     This view allows users to log in by providing their username/email and password.
#     Upon successful login, an authentication token is generated and returned.
#
#     Request:
#     - POST data: {'username': 'user1', 'password': 'password'}
#     - POST data optional: {'email': 'user1@neofi.com', 'username': 'user1', 'password': 'password'}
#
#     Response (successful login):
#     - Status Code: 200 (OK)
#     - Response Data:
#         {
#             'message': 'Login successful',
#             'token': 'your-auth-token-string'
#         }
#     """
#
#     permission_classes = [AllowAny]
#     serializer_class = UserLoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         # Create or retrieve an authentication token for the user
#         access_token = serializer.validated_data.get('access_token')
#
#         if access_token:
#             return Response(
#                 {'message': 'Login successful', 'access_token': access_token},
#                 status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 {'message': 'Login failed or something went wrong!', 'access_token': None},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
#
#
# class UserUpdateView(UpdateAPIView):
#     """
#     View for updating user details.
#
#     This view allows authenticated users to update their user details.
#
#     Request (authenticated user):
#     - PATCH data: {
#         'first_name': 'NewFirstName',
#         'last_name': 'NewLastName',
#         'contact_number': 'NewContactNumber',
#         'gender': 'new_gender',
#         'birth_date': 'new_birth_date'
#       }
#
#     Response (successful update):
#     - Status Code: 200 (OK)
#     - Response Data: {'message': 'User data updated successfully', 'data': Updated user details}
#
#     Response (failed update):
#     - Status Code: 400 (Bad Request)
#     - Response Data: Validation errors
#     """
#     queryset = Users.objects.all()
#     serializer_class = UserUpdateSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):
#         return self.request.user
#
#     def patch(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {'message': 'User data updated successfully', 'data': serializer.data},
#             status=status.HTTP_200_OK
#         )
#
#
# class UserLogoutView(APIView):
#
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         user_obj = request.user
#         if user_obj:
#             user_obj.is_online = False
#             user_obj.save()
#             return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
