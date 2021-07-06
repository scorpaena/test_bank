from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.http import Http404
from django.contrib.auth.models import User
from datetime import date
from apps.account.exceptions import (
    TransferValidationError, 
    BalanceValidationError
)
from apps.account.models import Account, MoneyTransferLog
from apps.account.services import (
    get_account,
    get_account_for_transfer, 
    is_transfer_valid,
    money_transfer,
    to_money_transfer_log
)

today = date.today()


class MoneyTransferTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='foo1',
            password='bar1'
        )
        self.user2 = User.objects.create_user(
            username='foo2',
            password='bar2'
        )
        
        self.account1 = Account.objects.create(
            account = 'debit',
            currency = 'USD',
            balance = 100,
            created_at = today,
            user = self.user1
        )
        self.account2 = Account.objects.create(
            account = 'debit',
            currency = 'USD',
            balance = 100,
            created_at = today,
            user = self.user2
        )

    def test_get_account(self):
        self.assertEqual(get_account(account = 1), self.account1)

    def test_get_account_for_transfer(self):
        self.assertEqual(get_account_for_transfer(account = 1), self.account1)

    def test_is_transfer_valid(self):
        self.assertTrue(
            is_transfer_valid(
                account_from = 1, 
                account_to = 2, 
                amount = 10
            )
        )

    def test_is_transfer_valid_same_account(self):
        with self.assertRaises(TransferValidationError):
            is_transfer_valid(
                account_from = 1, 
                account_to = 1, 
                amount = 10
            )

    def test_is_transfer_valid_negative_balance(self):
        with self.assertRaises(BalanceValidationError):
            is_transfer_valid(
                account_from = 1, 
                account_to = 2, 
                amount = 101
            )

    def test_money_transfer(self):
        money_transfer(
            account_from = 1,
            account_to = 2,
            amount = 10
            )
        self.assertEqual(get_account(2).balance - get_account(1).balance, 20)

    def test_to_money_transfer_log(self):
        log_instance = to_money_transfer_log(
            account_from = 1,
            account_to = 2,
            user = self.user1,
            amount = 10
        )
        self.assertTrue(isinstance(log_instance, MoneyTransferLog))