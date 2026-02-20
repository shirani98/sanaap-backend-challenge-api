from django.urls import path
from apps.user.api.views import LoginView, RefreshTokenView, LogoutView

urlpatterns = [
    path("login/", LoginView.as_view(), name="auth-login"),
    path("token/refresh/", RefreshTokenView.as_view(), name="auth-token-refresh"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
]
