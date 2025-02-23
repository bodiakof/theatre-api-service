from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.serializers import UserSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """Endpoint for user registration."""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Endpoint for retrieving and updating the authenticated user."""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_object(self) -> User:
        """Returns the authenticated user instance."""
        return self.request.user
