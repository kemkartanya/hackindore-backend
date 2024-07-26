from django.urls import path
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

from .views import (
    UserProfileView,
    UpdatePasswordView,
)


urlpatterns = [
    path("user/", UserProfileView.as_view(), name="user-profile"),
    path("user/password/", UpdatePasswordView.as_view(), name="update-password"),
    path("password-reset/", PasswordResetView.as_view()),
    path(
        "password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]