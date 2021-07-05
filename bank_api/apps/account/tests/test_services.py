from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.http import Http404
from django.contrib.auth.models import User
from datetime import date
from apps.account.models import Account, MoneyTransferLog
from apps.account.services import (
    get_account_to, 
    is_account_to_valid,
    money_transfer,
    to_money_transfer_log
)

today = date.today()


class MoneyTransferTest(TestCase):

    def setUp(self):
        self.customer1 = User.objects.create_user(
            username='foo1',
            password='bar1'
        )
        self.customer2 = User.objects.create_user(
            username='foo2',
            password='bar2'
        )
        
        self.account_payload1 = {
            'account': 'debit',
            'currency': 'USD',
            'balance': 100,
            'created_at': today,
            'customer': self.customer1
        }
        self.account_payload2 = {
            'account': 'debit',
            'currency': 'USD',
            'balance': 100,
            'created_at': today,
            'customer': self.customer2
        }

        self.account1 = Account.objects.create(**self.account_payload1)
        self.account2 = Account.objects.create(**self.account_payload2)

        self.money_transfer_payload = {
            'account_from': self.account1,
            'account_to': 2,
            'amount': 10
        }

        self.money_transfer_log_payload = {
            'account_from': self.account1,
            'account_to': 2,
            'customer': self.customer1,
            'created_at': today,
            'amount': 10
        }

    def test_get_account_to(self):
        self.assertEqual(get_account_to(self.account1.id), self.account1)

    def test_get_account_to_404(self):
        with self.assertRaises(Http404):
            get_account_to(self.account1.id+2)

    def test_is_account_to_valid(self):
        self.assertTrue(is_account_to_valid(self.account1, self.account2.id))

    def test_is_account_to_valid_negative(self):
        self.assertFalse(is_account_to_valid(self.account1, self.account1.id))

    def test_money_transfer(self):
        money_transfer(**self.money_transfer_payload)
        self.assertEqual(
            get_account_to(account_to=2).balance - self.account1.balance, 
            self.money_transfer_payload['amount'] * 2
        )

    def test_money_transfer_negative(self):
        self.money_transfer_payload['amount'] = 101
        with self.assertRaises(ValidationError):
            money_transfer(**self.money_transfer_payload)

    def test_to_money_transfer_log(self):
        log_instance = to_money_transfer_log(**self.money_transfer_log_payload)
        self.assertTrue(isinstance(log_instance, MoneyTransferLog))