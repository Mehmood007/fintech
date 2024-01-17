from django.urls import path

from .views import AccountView, KYCRegistrationView

urlpatterns = [
    path("", AccountView.as_view(), name="account"),
    path("kyc-registration", KYCRegistrationView.as_view(), name="kyc-registration"),
]
