from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            'name', 
            'color',
            'amount',
            'code',
            'kind',
            'is_favorite',
            'is_hide',
        )