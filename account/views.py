import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from core.models import Transaction
from fintech.utils import KYCExistsMixin

from .forms import KYCForm
from .models import KYC, Account

logger = logging.getLogger("custom_logger")


# "/account"
@method_decorator(login_required, name="dispatch")
class AccountView(KYCExistsMixin, View):
    def get(self, request: HttpRequest) -> render:
        self.account = Account.objects.get(user=request.user)
        context = {
            "account": self.account,
            "kyc": self.kyc,
        }
        return render(request, "account/account.html", context)


# "/account/kyc-registration"
@method_decorator(login_required, name="dispatch")
class KYCRegistrationView(View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.kyc = KYC.objects.filter(user=request.user).first()
        self.account = Account.objects.get(user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> render:
        form = KYCForm(instance=self.kyc)
        context = {
            "form": form,
            "account": self.account,
        }
        return render(request, "account/kyc-form.html", context)

    def post(self, request: HttpRequest) -> redirect or render:
        form = KYCForm(request.POST, request.FILES, instance=self.kyc)
        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.user = request.user
            kyc.account = self.account
            kyc.save()
            messages.success(request, "KYC form saved successfully. In review now...")
            return redirect("home")

        messages.error(request, "Sorry could not save your kyc")
        logger.error(form.errors)
        context = {
            "form": form,
            "account": self.account,
        }
        return render(request, "account/kyc-form.html", context)


# "/account/dashboard"
@method_decorator(login_required, name="dispatch")
class DashboardView(KYCExistsMixin, View):
    def get(self, request: HttpRequest) -> render:
        account = Account.objects.get(user=request.user)
        sender_transaction = Transaction.objects.filter(sender=request.user)
        receiver_transaction = Transaction.objects.filter(reciever=request.user)
        context = {
            "account": account,
            "sender_transaction": sender_transaction,
            "receiver_transaction": receiver_transaction,
        }
        return render(request, "account/dashboard.html", context)
