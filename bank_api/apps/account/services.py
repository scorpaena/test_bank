from django.db import transaction
from .models import MoneyTransferLog
from .exceptions import TransferValidationError, BalanceValidationError


def is_transfer_valid(account_from, account_to, amount):
    if account_from == account_to:
        raise TransferValidationError(account_from, account_to)
    if account_from.balance < amount:
        raise BalanceValidationError(account_from.balance, amount)
    return True


def money_transfer(account_from, account_to, amount):
    is_transfer_valid(account_from, account_to, amount)
    with transaction.atomic():
        account_from.balance -= amount
        account_to.balance += amount
        account_from.save()
        account_to.save()


def to_money_transfer_log(account_from, account_to, user, amount):
    return MoneyTransferLog.objects.create(
        account_from=account_from, account_to=account_to, user=user, amount=amount
    )
