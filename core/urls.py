from django.urls import path

from .views import (
    AmountTransferView,
    DeclineTransferRequestView,
    DeleteTransferRequestView,
    RequestAmountTransferView,
    RequestCompletedView,
    RequestSearchUserView,
    SearchUserView,
    SettlementConfirmationView,
    TransactionDetailsView,
    TransactionsHistoryView,
    TransferCompletedView,
    TransferConfirmView,
    TransferRequestConfirmView,
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
    # Request Payments
    path(
        "request-search-user",
        RequestSearchUserView.as_view(),
        name="request-search-user",
    ),
    path(
        "request-amount-transfer/<int:account_number>",
        RequestAmountTransferView.as_view(),
        name="request-amount-transfer",
    ),
    path(
        "transfer-request-confirm/<int:account_number>/<str:transaction_id>",
        TransferRequestConfirmView.as_view(),
        name="transfer-request-confirm",
    ),
    path(
        "request-completed/<int:account_number>/<str:transaction_id>",
        RequestCompletedView.as_view(),
        name="request-completed",
    ),
    # Settlements
    path(
        "settlement-confirmation/<int:account_number>/<str:transaction_id>",
        SettlementConfirmationView.as_view(),
        name="settlement-confirmation",
    ),
    path(
        "delete-request/<transaction_id>",
        DeleteTransferRequestView.as_view(),
        name="delete-request",
    ),
    path(
        "decline-request/<transaction_id>",
        DeclineTransferRequestView.as_view(),
        name="decline-request",
    ),
]
