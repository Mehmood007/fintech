from django.urls import path

from .views import AccountView, DashboardView, KYCRegistrationView

urlpatterns = [
    path("", AccountView.as_view(), name="account"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("kyc-registration", KYCRegistrationView.as_view(), name="kyc-registration"),
]
