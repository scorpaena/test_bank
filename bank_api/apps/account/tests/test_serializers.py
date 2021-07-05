from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from apps.account.serializers import MoneyTransferSerializer
from apps.account.models import Account, MoneyTransferLog
from datetime import date

today = date.today()


class MoneyTransferSerializerTest(TestCase):
    
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
            'customer': self.customer1,
            'created_at': today,
            'amount': 10
        }

    def test_money_transfer_serializer(self):
        money_transfer = MoneyTransferSerializer(data=self.money_transfer_payload)
        self.assertTrue(money_transfer.is_valid())

    def test_money_transfer_serializer_update(self):
        money_transfer = MoneyTransferSerializer(data=self.money_transfer_payload)
        money_transfer.update(money_transfer, self.money_transfer_payload)
        self.assertEqual(
            MoneyTransferLog.objects.get(id=1).customer.username, self.customer1.username
        )

    def test_money_transfer_serializer_update_negative(self):
        money_transfer = MoneyTransferSerializer(data=self.money_transfer_payload)
        self.money_transfer_payload['account_to'] = 1
        with self.assertRaises(ValidationError):
            money_transfer.update(money_transfer, self.money_transfer_payload)
        with self.assertRaises(ObjectDoesNotExist):
            MoneyTransferLog.objects.get(id=1)
