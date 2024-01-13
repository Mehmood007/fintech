from django.urls import path

from .views import LogInView, LogoutView, RegistrationView

urlpatterns = [
    path("signup", RegistrationView.as_view(), name="signup"),
    path("login", LogInView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
]
