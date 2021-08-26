import wallets
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection, transaction, models
from rest_framework import viewsets, filters
from rest_framework.response import Response

from .models import Wallet
from .serializers import WalletSerializer

from transactions.models import Transaction
from items.models import Item


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def list(self, request):
        queryset = Wallet.objects.all()
        serializer = WalletSerializer(queryset, many=True, context=self.amount_sum())
        return Response(serializer.data)

    def amount_sum(self):
        wallets_expenses = Item.objects.values('transaction__wallet_expenses').annotate(amount=models.Sum('amount_expenses'))
        wallets_income = Item.objects.values('transaction__wallet_income').annotate(amount=models.Sum('amount_income'))
        return {'income':wallets_income, 'expenses':wallets_expenses}

def index(request):
    latest_question_list = Wallet.objects

    return HttpResponse(latest_question_list)