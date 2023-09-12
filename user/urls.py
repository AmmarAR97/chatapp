from django.urls import path
from .views import (UserRegistrationView, UserLoginView)


urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(), name='user_registration'),
    path('api/login/', UserLoginView.as_view(), name='user_login'),
    # path('api/online-user/', UserRegistrationView.as_view(), name='online_users'),
    # path('api/suggested–friends/<int:user_id>/', UserRegistrationView.as_view(), name='suggested–friends')
]
