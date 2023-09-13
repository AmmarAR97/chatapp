from django.utils import timezone
from django.contrib.sessions.middleware import SessionMiddleware
from user.models import Users


# class CustomSessionMiddleware(SessionMiddleware):
#
#     def process_request(self, request):
#         super().process_request(request)
#         # Update the user's last_activity timestamp if the user is authenticated
#         if request.user.is_authenticated:
#             Users.objects.filter(pk=request.user.pk).update(last_activity=timezone.now())
