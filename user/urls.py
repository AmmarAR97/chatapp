from django.urls import path
from .views import (UserRegistrationView, UserLoginView, UserUpdateView, UserLogoutView, SuggestedFriendsView)


urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(), name='user_registration'),
    path('api/login/', UserLoginView.as_view(), name='user_login'),
    path('api/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('api/update-data/', UserUpdateView.as_view(), name='user_data_update'),
    path('api/suggested–friends/<int:user_id>/', SuggestedFriendsView.as_view(), name='suggested–friends')
]
