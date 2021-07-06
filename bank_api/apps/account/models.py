from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    
    DEB = 'deb'
    CRE = 'cre'
    DEP = 'dep'
    
    TYPE = [
        (DEB, 'debit'),
        (CRE, 'credit'),
        (DEP, 'deposit'),
    ]

    account = models.CharField(max_length=7, choices=TYPE, default=DEB)
    currency = models.CharField(max_length=3, default='USD')
    balance = models.PositiveIntegerField(default = 100)
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}_{self.user.username}'


class MoneyTransferLog(models.Model):
    
    account_from = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_from')
    account_to = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_to')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    amount = models.PositiveIntegerField(default=10)
