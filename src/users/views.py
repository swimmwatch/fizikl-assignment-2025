from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions

from users.serializers import UserSerializer

User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    """
    View for registering new users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
