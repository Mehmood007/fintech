from django.contrib import admin

from .models import CreditCard, Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "amount",
        "status",
        "transaction_type",
        "reciever",
        "sender",
    ]
    list_editable = ["amount", "status", "transaction_type", "reciever", "sender"]


class CreditCardAdmin(admin.ModelAdmin):
    list_display = ["user", "amount", "card_type"]
    list_editable = ["amount", "card_type"]


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
