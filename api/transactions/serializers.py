from rest_framework import serializers

from .models import Transaction
from wallets.serializers import WalletSerializer
from items.serializers import ItemSerializer


class TransactionSerializer(serializers.ModelSerializer):
    wallet_expenses = WalletSerializer()
    wallet_income = WalletSerializer()
    items = ItemSerializer(many=True, read_only=True)

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
            'items',
        )