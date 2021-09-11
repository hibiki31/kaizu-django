from django_filters import rest_framework as filters
from django.core import serializers
from django.db import connection, transaction, models
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
import json
from .models import Transaction, Supplier
from items.models import Item, Category
from .serializers import TransactionSerializer, SupplierSerializer


class SupplierFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='contains')

    class Meta:
        model = Supplier
        fields = ['name']


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = Transaction.objects.order_by('date').reverse().all()
        if (name := self.request.query_params.get('name')) is not None:
            queryset = queryset.filter(items__name__icontains=name)
        if (supplier := self.request.query_params.get('supplier')) is not None:
            queryset = queryset.filter(supplier__name__icontains=supplier)
        if (category := self.request.query_params.get('category')) is not None:
            queryset = queryset.filter(items__sub_category__category__pk=category)
        if (subcategory := self.request.query_params.get('subcategory')) is not None:
            queryset = queryset.filter(items__sub_category__pk=subcategory)
        if (wallet := self.request.query_params.get('wallet')) is not None:
            queryset = queryset.filter(Q(wallet_income=wallet) | Q(wallet_expenses=wallet))
        if (kind := self.request.query_params.get('kind')) is not None:
            queryset = queryset.filter(kind=kind)
        return queryset


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    pagination_class = None
    filter_class = SupplierFilter


class CategorySummaryView(APIView):
    def get(self, request, format=None):
        
        transaction = Item.objects.filter(
                transaction__date__year='2020', 
                transaction__date__month='01'
            ).values(
            category_name=models.F('sub_category__category__name'), 
            category_id=models.F('sub_category__category__pk')
            ).annotate(
                amount=models.Sum('amount_expenses')
            ).all()
        
        sum_dict = {}

        for i in transaction:
            sum_dict[i['category_id']] = i["amount"]
        
        print(sum_dict)
        
        category = Category.objects.all()

        result_list = []
        for i in category:
            result_list.append(
                {
                    "name": i.name,
                    "color": i.color,
                    "summary": sum_dict.get(i.pk,0)
                }
            )



        
        return Response(result_list)
        return Response(json.loads(serializers.serialize('json', transaction)))