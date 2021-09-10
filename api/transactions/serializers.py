from items.models import Item
from wallets.models import Wallet
from rest_framework import serializers

from .models import Supplier, Transaction
from wallets.serializers import WalletSerializer
from items.serializers import ItemSerializer


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = (
            'pk',
            'name',
        )


class TransactionSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), write_only=True)
    wallet_income = WalletSerializer(read_only=True)
    wallet_income_id = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all(), write_only=True)
    wallet_expenses = WalletSerializer(read_only=True)
    wallet_expenses_id = serializers.PrimaryKeyRelatedField(queryset=Wallet.objects.all(), write_only=True)
    

    def create(self, validated_data):
        validated_data['supplier'] = validated_data.get('supplier_id', None)
        validated_data['wallet_income'] = validated_data.get('wallet_income_id', None)
        validated_data['wallet_expenses'] = validated_data.get('wallet_expenses_id', None)

        if validated_data['supplier'] is None:
            raise serializers.ValidationError("supplier not found.") 
        
        if validated_data['wallet_income'] is None:
            raise serializers.ValidationError("wallet not found.")
        
        if validated_data['wallet_expenses'] is None:
            raise serializers.ValidationError("wallet not found.") 

        del validated_data['supplier_id']
        del validated_data['wallet_income_id']
        del validated_data['wallet_expenses_id']

        # POSTされたアイテムを分離
        items_data = validated_data.pop('items')
        # トランザクションを作成
        transaction = Transaction.objects.create(**validated_data)
        # トランザクションを外部キー指定でアイテムを作成
        for item_data in items_data:
            item_data['sub_category'] = item_data.get('sub_category_id', None)
        
            if item_data['sub_category'] is None:
                raise serializers.ValidationError("sub_cateory not found.")

            del item_data['sub_category_id']
            Item.objects.create(transaction=transaction, **item_data)
        return transaction

    class Meta:
        model = Transaction
        fields = (
            'pk',
            'kind',
            'supplier',
            'supplier_id',
            'date',
            'wallet_expenses',
            'wallet_expenses_id',
            'wallet_income',
            'wallet_income_id',
            'items',
        )
