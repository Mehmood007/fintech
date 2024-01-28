from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from account.models import KYC, Account


class NotLoggedInMixin:
    """
    User must not be logged in order to visit specific page
    """

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect("account")
        return super().dispatch(request, *args, **kwargs)


class KYCExistsMixin:
    """
    User must have filled KYC form before specific requests to process
    """

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            self.kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "Please Fill out KYC form")
            return redirect("kyc-registration")
        return super().dispatch(request, *args, **kwargs)
