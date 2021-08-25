from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, filters

from .models import Wallet
from .serializers import WalletSerializer



class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

def index(request):
    latest_question_list = Wallet.objects

    return HttpResponse(latest_question_list)