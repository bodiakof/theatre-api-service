from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from user.serializers import UserSerializer


User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """Endpoint for user registration."""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Endpoint for retrieving and updating the authenticated user."""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        """Returns the authenticated user instance."""
        return self.request.user
