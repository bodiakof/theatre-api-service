from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from user.views import CreateUserView, ManageUserView


app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("me/", ManageUserView.as_view(), name="manage"),

    path("token/", include([
        path("obtain/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    ])),
]
