from django.db import transaction
from .models import Account, MoneyTransferLog
from .exceptions import TransferValidationError, BalanceValidationError

def get_account(account):
    return Account.objects.get(id=account)

def get_account_for_transfer(account):
    return Account.objects.select_for_update().get(id=account)

def is_transfer_valid(account_from, account_to, amount):
    account_from = get_account(account_from)
    account_to = get_account(account_to)
    if account_from == account_to:
        raise TransferValidationError
    if account_from.balance < amount:
        raise BalanceValidationError
    return True

def money_transfer(account_from, account_to, amount):
    is_transfer_valid(account_from, account_to, amount)
    with transaction.atomic():
        account_from = get_account_for_transfer(account_from)
        account_to = get_account_for_transfer(account_to)
        account_from.balance -= amount
        account_to.balance += amount
        account_from.save()
        account_to.save()

def to_money_transfer_log(account_from, account_to, user, amount):
    account_from = get_account(account_from)
    account_to = get_account(account_to)
    return MoneyTransferLog.objects.create(
        account_from=account_from,
        account_to=account_to,
        user=user,
        amount=amount
    )
