from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from apps.account.exceptions import TransferValidationError, BalanceValidationError
from apps.account.models import Account
from apps.account.services import (
    is_transfer_valid,
    money_transfer,
)

today = date.today()


class MoneyTransferTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="foo1", password="bar1")
        self.user2 = User.objects.create_user(username="foo2", password="bar2")

        self.account1 = Account.objects.create(
            account="debit",
            currency="USD",
            balance=100,
            created_at=today,
            user=self.user1,
        )
        self.account2 = Account.objects.create(
            account="debit",
            currency="USD",
            balance=100,
            created_at=today,
            user=self.user2,
        )

    def test_is_transfer_valid(self):
        self.assertTrue(
            is_transfer_valid(
                account_from=self.account1, account_to=self.account2, amount=10
            )
        )

    def test_is_transfer_valid_same_account(self):
        with self.assertRaises(TransferValidationError):
            is_transfer_valid(
                account_from=self.account1, account_to=self.account1, amount=10
            )

    def test_is_transfer_valid_negative_balance(self):
        with self.assertRaises(BalanceValidationError):
            is_transfer_valid(
                account_from=self.account1, account_to=self.account2, amount=101
            )

    def test_money_transfer(self):
        money_transfer(account_from=self.account1, account_to=self.account2, amount=10)
        self.assertEqual(self.account2.balance - self.account1.balance, 20)
