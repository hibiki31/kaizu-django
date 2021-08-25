from rest_framework import serializers

from .models import Transaction
from wallets.serializers import WalletSerializer


class TransactionSerializer(serializers.ModelSerializer):
    wallet_expenses = WalletSerializer()
    wallet_income = WalletSerializer()

    class Meta:
        model = Transaction
        fields = (
            'pk',
            'shop', 
            'provider',
            'provider_id',
            'date',
            'wallet_expenses',
            'wallet_income',
        )