from django.urls import path

from core_apps.users.views import (
    UserLoginAPI,
    UserLogOutAPIView,
    UserRegistrationAPI,
    UserTokenObtainPairView,
)

urlpatterns = [
    path(
        "signup/",
        UserRegistrationAPI.as_view(),
        name="api_user_signup",
    ),
    path("login/", UserLoginAPI.as_view(), name="api_user_login"),
    path("logout/", UserLogOutAPIView.as_view(), name="api_user_logout"),
    path("get-token/", UserTokenObtainPairView.as_view(), name="get_token"),
]
