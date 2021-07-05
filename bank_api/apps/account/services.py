from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Account, MoneyTransferLog

def get_account_to(account_to):
    return get_object_or_404(Account, pk=account_to)

def is_account_to_valid(account_from, account_to):
    account_to = get_account_to(account_to)
    return account_to != account_from

def money_transfer(account_from, account_to, amount):
    account_to = get_account_to(account_to)
    account_from.balance -= amount
    account_to.balance += amount
    if account_from.balance >= 0:
        account_from.save()
        account_to.save()
    else:
        raise ValidationError ("you don't have enough money")

def to_money_transfer_log(**validated_data):
    validated_data['account_to'] = get_account_to(validated_data['account_to'])
    return MoneyTransferLog.objects.create(**validated_data)
