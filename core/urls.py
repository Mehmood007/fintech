from django.urls import path

from .views import (
    AmountTransferView,
    SearchUserView,
    TransactionDetailsView,
    TransactionsHistoryView,
    TransferCompletedView,
    TransferConfirmView,
)

urlpatterns = [
    path("search-user", SearchUserView.as_view(), name="search-user"),
    path(
        "amount-transfer/<int:account_number>",
        AmountTransferView.as_view(),
        name="amount-transfer",
    ),
    path(
        "transfer-confirm/<int:account_number>/<str:transaction_id>",
        TransferConfirmView.as_view(),
        name="transfer-confirm",
    ),
    path(
        "transfer-completed/<int:account_number>/<str:transaction_id>",
        TransferCompletedView.as_view(),
        name="transfer-completed",
    ),
    path(
        "transaction-history",
        TransactionsHistoryView.as_view(),
        name="transaction-history",
    ),
    path(
        "transaction-details/<transaction_id>",
        TransactionDetailsView.as_view(),
        name="transaction-details",
    ),
]
