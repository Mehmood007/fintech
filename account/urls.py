from django.urls import path

from .views import KYCRegistrationView

urlpatterns = [
    path("kyc-registration", KYCRegistrationView.as_view(), name="kyc-registration"),
]
