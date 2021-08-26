from django.db import models
from wallets.models import Wallet

class Transaction(models.Model):
    shop = models.CharField(max_length=256)
    provider = models.CharField(max_length=256)
    provider_id = models.CharField(max_length=256)
    date = models.DateTimeField()
    wallet_expenses = models.ForeignKey(Wallet, related_name='transactions_expenses', on_delete=models.CASCADE)
    wallet_income = models.ForeignKey(Wallet, related_name='transactions_income', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}: {str(self.date)} {self.shop}'
    
    __repr__ = __str__