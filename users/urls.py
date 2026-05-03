from django.urls import path

from .views import (
    StyledPasswordResetCompleteView,
    StyledPasswordResetConfirmView,
    StyledPasswordResetDoneView,
    StyledPasswordResetView,
    login_view,
    logout_view,
    set_language_view,
    register_view,
)

app_name = "users"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("set-language/", set_language_view, name="set_language"),
    path("password-reset/", StyledPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", StyledPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", StyledPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/complete/", StyledPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
