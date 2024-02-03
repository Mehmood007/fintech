from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from account.models import Account
from fintech.utils import KYCExistsMixin

from .models import Transaction


# "core/search-user"
@method_decorator(login_required, name="dispatch")
class SearchUserView(KYCExistsMixin, View):
    def get(self, request: HttpRequest) -> render:
        accounts = Account.objects.all().order_by("?")[:5]
        context = {
            "accounts": accounts,
        }
        return render(request, "core/search-user.html", context)

    def post(self, request: HttpRequest) -> render:
        query = request.POST.get("account_number")
        context = {}
        if query:
            accounts = Account.objects.filter(
                Q(account_number=int(query)) | Q(account_id=query)
            ).distinct()
            context = {
                "accounts": accounts,
            }
        return render(request, "core/search-user.html", context)


# "core/amount-transfer/<int:account_number>"
@method_decorator(login_required, name="dispatch")
class AmountTransferView(KYCExistsMixin, View):
    def dispatch(self, request: HttpRequest, account_number: int) -> HttpResponse:
        self.account_number = account_number
        try:
            self.account = Account.objects.get(account_number=account_number)
        except:
            messages.warning(request, "No such account exists")
            return redirect("search-user")
        return super().dispatch(request)

    def get(self, request: HttpRequest) -> render:
        context = {"account": self.account}
        return render(request, "core/amount-transfer.html", context)

    def post(self, request: HttpRequest) -> render:
        sender = request.user
        receiver = self.account.user
        amount = Decimal(request.POST.get("amount-send"))
        description = request.POST.get("description")

        if amount > 0 and sender.account.account_balance > amount:
            new_transaction = Transaction.objects.create(
                user=sender,
                amount=amount,
                description=description,
                reciever=receiver,
                sender=sender,
                sender_account=sender.account,
                reciever_account=self.account,
                status="processing",
                transaction_type="transfer",
            )
            new_transaction.save()
            transaction_id = new_transaction.transaction_id
            return redirect("transfer-confirm", self.account_number, transaction_id)

        messages.warning(request, "You don't have sufficient balance")
        context = {"account": self.account}
        return render(request, "core/amount-transfer.html", context)


# "core/transfer-confirm/<int:account_number>/<transaction_id>"
@method_decorator(login_required, name="dispatch")
class TransferConfirmView(KYCExistsMixin, View):
    def dispatch(
        self, request: HttpRequest, account_number: int, transaction_id: str
    ) -> HttpResponse:
        self.transaction_id = transaction_id
        self.account_number = account_number
        try:
            self.account = Account.objects.get(account_number=account_number)
            self.transaction = Transaction.objects.get(transaction_id=transaction_id)
        except:
            messages.warning(request, "No such transaction exists")
            return redirect("search-user")
        return super().dispatch(request)

    def get(self, request: HttpRequest) -> render:
        context = {
            "account": self.account,
            "transaction": self.transaction,
        }
        return render(request, "core/transfer-confirm.html", context)

    def post(self, request: HttpRequest) -> render:
        sender = request.user
        receiver = self.account.user
        sender_account = sender.account

        pin = request.POST.get("pin-number")

        if pin == sender_account.pin_number:
            self.transaction.status = "completed"
            self.transaction.save()

            sender_account.account_balance -= self.transaction.amount
            sender_account.save()

            self.account.account_balance += self.transaction.amount
            self.account.save()

            messages.success(request, "Transaction completed successfully")
            return redirect(
                "transfer-completed", self.account_number, self.transaction_id
            )

        messages.warning(request, "Invalid Pin")
        return redirect(request.get_full_path())


# "core/transfer-completed/<int:account_number>/<transaction_id>"
@method_decorator(login_required, name="dispatch")
class TransferCompletedView(KYCExistsMixin, View):
    def dispatch(
        self, request: HttpRequest, account_number: int, transaction_id: str
    ) -> HttpResponse:
        try:
            self.account = Account.objects.get(account_number=account_number)
            self.transaction = Transaction.objects.get(transaction_id=transaction_id)
        except:
            messages.warning(request, "No such transaction exists")
            return redirect("search-user")
        return super().dispatch(request)

    def get(self, request: HttpRequest) -> render:
        context = {
            "account": self.account,
            "transaction": self.transaction,
        }
        return render(request, "core/transfer-completed.html", context)


# "/core/transaction-history"
@method_decorator(login_required, name="dispatch")
class TransactionsHistoryView(KYCExistsMixin, View):
    def get(self, request: HttpRequest) -> render:
        account = Account.objects.get(user=request.user)

        sender_transaction = Transaction.objects.filter(
            sender=request.user, transaction_type="transfer"
        ).order_by("-updated_at")
        receiver_transaction = Transaction.objects.filter(
            reciever=request.user, transaction_type="transfer"
        ).order_by("-updated_at")

        request_sender_transaction = Transaction.objects.filter(
            reciever=request.user, transaction_type="request"
        ).order_by("-updated_at")
        request_receiver_transaction = Transaction.objects.filter(
            sender=request.user, transaction_type="request"
        ).order_by("-updated_at")

        context = {
            "account": account,
            "sender_transaction": sender_transaction,
            "receiver_transaction": receiver_transaction,
            "request_sender_transaction": request_sender_transaction,
            "request_receiver_transaction": request_receiver_transaction,
        }
        return render(request, "transaction/transaction-history.html", context)


# "/core/transaction-details/<transaction_id>"
@method_decorator(login_required, name="dispatch")
class TransactionDetailsView(KYCExistsMixin, View):
    def get(self, request: HttpRequest, transaction_id: str) -> render:
        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
        except:
            messages.warning(request, "No such transaction exists")
            return redirect("account")

        context = {
            "transaction": transaction,
        }
        return render(request, "transaction/transaction-details.html", context)


# "core/request-search-user"
@method_decorator(login_required, name="dispatch")
class RequestSearchUserView(KYCExistsMixin, View):
    def get(self, request: HttpRequest) -> render:
        accounts = Account.objects.all().order_by("?")[:5]
        context = {
            "accounts": accounts,
        }
        return render(request, "core/request-search-user.html", context)

    def post(self, request: HttpRequest) -> render:
        query = request.POST.get("account_number")
        context = {}
        if query:
            accounts = Account.objects.filter(
                Q(account_number=int(query)) | Q(account_id=query)
            ).distinct()
            context = {
                "accounts": accounts,
            }
        return render(request, "core/request-search-user.html", context)


# "core/request-amount-transfer/<int:account_number>"
@method_decorator(login_required, name="dispatch")
class RequestAmountTransferView(KYCExistsMixin, View):
    def dispatch(self, request: HttpRequest, account_number: int) -> HttpResponse:
        self.account_number = account_number
        try:
            self.account = Account.objects.get(account_number=account_number)
        except:
            messages.warning(request, "No such account exists")
            return redirect("request-search-user")
        return super().dispatch(request)

    def get(self, request: HttpRequest) -> render:
        context = {"account": self.account}
        return render(request, "core/request-amount-transfer.html", context)

    def post(self, request: HttpRequest) -> render:
        sender = self.account.user
        receiver = request.user
        amount = Decimal(request.POST.get("amount-request"))
        description = request.POST.get("description")

        new_transaction = Transaction.objects.create(
            user=sender,
            amount=amount,
            description=description,
            reciever=receiver,
            sender=sender,
            sender_account=sender.account,
            reciever_account=receiver.account,
            status="request_processing",
            transaction_type="request",
        )
        new_transaction.save()
        transaction_id = new_transaction.transaction_id
        return redirect("transfer-request-confirm", self.account_number, transaction_id)


# "core/transfer-request-confirm/<int:account_number>/<transaction_id>"
@method_decorator(login_required, name="dispatch")
class TransferRequestConfirmView(KYCExistsMixin, View):
    def dispatch(
        self, request: HttpRequest, account_number: int, transaction_id: str
    ) -> HttpResponse:
        self.transaction_id = transaction_id
        self.account_number = account_number
        try:
            self.account = Account.objects.get(account_number=account_number)
            self.transaction = Transaction.objects.get(transaction_id=transaction_id)
            if self.transaction.reciever != request.user:
                messages.warning(request, "Sorry you are not allowed for this request")
                return redirect("request-search-user")
        except:
            messages.warning(request, "No such transaction exists")
            return redirect("request-search-user")
        return super().dispatch(request)

    def get(self, request: HttpRequest) -> render:
        context = {
            "account": self.account,
            "transaction": self.transaction,
        }
        return render(request, "core/transfer-request-confirm.html", context)

    def post(self, request: HttpRequest) -> render:

        pin = request.POST.get("pin-number")

        if pin == self.transaction.reciever_account.pin_number:
            self.transaction.status = "request_sent"
            self.transaction.save()

            messages.success(request, "Your request has been sent successfully")
            return redirect(
                "request-completed", self.account_number, self.transaction_id
            )

        messages.warning(request, "Invalid Pin")
        return redirect(request.get_full_path())


# "core/request-completed/<int:account_number>/<transaction_id>"
@method_decorator(login_required, name="dispatch")
class RequestCompletedView(KYCExistsMixin, View):
    def dispatch(
        self, request: HttpRequest, account_number: int, transaction_id: str
    ) -> HttpResponse:
        try:
            self.account = Account.objects.get(account_number=account_number)
            self.transaction = Transaction.objects.get(
                transaction_id=transaction_id, status="request_sent"
            )
        except:
            messages.warning(request, "No such transaction exists")
            return redirect("search-user")
        return super().dispatch(request)

    def get(self, request: HttpRequest) -> render:
        context = {
            "account": self.account,
            "transaction": self.transaction,
        }
        return render(request, "core/request-completed.html", context)


# "core/settlement-confirmation/<int:account_number>/<transaction_id>"
@method_decorator(login_required, name="dispatch")
class SettlementConfirmationView(KYCExistsMixin, View):
    def dispatch(
        self, request: HttpRequest, account_number: int, transaction_id: str
    ) -> HttpResponse:
        self.transaction_id = transaction_id
        self.account_number = account_number
        try:
            self.account = Account.objects.get(account_number=account_number)
            self.transaction = Transaction.objects.get(transaction_id=transaction_id)
        except:
            messages.warning(request, "No such transaction exists")
            return redirect("search-user")
        return super().dispatch(request)

    def get(self, request: HttpRequest) -> render:
        context = {
            "account": self.account,
            "transaction": self.transaction,
        }
        return render(request, "core/settlement-confirmation.html", context)

    def post(self, request: HttpRequest) -> render:
        sender = request.user
        receiver = self.account.user
        sender_account = sender.account

        pin = request.POST.get("pin-number")

        if (
            pin == sender_account.pin_number
            and sender_account.account_balance >= self.transaction.amount
        ):
            self.transaction.status = "request_settled"
            self.transaction.save()

            sender_account.account_balance -= self.transaction.amount
            sender_account.save()

            self.account.account_balance += self.transaction.amount
            self.account.save()

            messages.success(request, "Transaction completed successfully")
            return redirect(
                "transfer-completed", self.account_number, self.transaction_id
            )

        messages.warning(request, "Invalid Pin")
        return redirect(request.get_full_path())


# "core/delete-request/<transaction_id>"
@method_decorator(login_required, name="dispatch")
class DeleteTransferRequestView(KYCExistsMixin, View):
    def dispatch(self, request: HttpRequest, transaction_id: str) -> HttpResponse:
        try:
            self.transaction = Transaction.objects.get(transaction_id=transaction_id)
        except:
            messages.warning(request, "No such transaction exists")
            return redirect("search-user")
        return super().dispatch(request)

    def get(self, request: HttpRequest) -> render:
        if self.transaction.reciever == request.user:
            self.transaction.delete()
            messages.success(request, "Transaction request deleted successfully")
        else:
            messages.warning(request, "Sorry you can not delete this request")
        return redirect("transaction-history")


# "core/decline-request/<transaction_id>"
@method_decorator(login_required, name="dispatch")
class DeclineTransferRequestView(KYCExistsMixin, View):
    def dispatch(self, request: HttpRequest, transaction_id: str) -> HttpResponse:
        try:
            self.transaction = Transaction.objects.get(transaction_id=transaction_id)
        except:
            messages.warning(request, "No such transaction exists")
            return redirect("search-user")
        return super().dispatch(request)

    def get(self, request: HttpRequest) -> render:
        if self.transaction.sender == request.user:
            self.transaction.status = "request_declined"
            self.transaction.save()
            messages.success(request, "Transaction request declined successfully")
        else:
            messages.warning(request, "Sorry you can not delete this request")
        return redirect("transaction-history")
