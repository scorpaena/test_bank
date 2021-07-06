from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError, NotFound
from apps.account.serializers import MoneyTransferSerializer
from apps.account.models import Account, MoneyTransferLog
from datetime import date

today = date.today()


class MoneyTransferSerializerTest(TestCase):
    
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

    def test_money_transfer_serializer(self):
        money_transfer = MoneyTransferSerializer(
            data = {
                'account_from': 1,
                'account_to': 2,
                'user': self.user1,
                'created_at': today,
                'amount': 10
            }
        )
        self.assertTrue(money_transfer.is_valid())

    def test_money_transfer_serializer_create(self):
        money_transfer = MoneyTransferSerializer()
        money_transfer.create(
            validated_data = {
                'account_from': 1,
                'account_to': 2,
                'user': self.user1,
                'created_at': today,
                'amount': 10
            }
        )
        self.assertEqual(
            MoneyTransferLog.objects.get(id=1).user.username, 
            self.user1.username
        )

    def test_money_transfer_serializer_create_same_account(self):
        money_transfer = MoneyTransferSerializer()
        with self.assertRaises(ValidationError):
            money_transfer.create(
                validated_data = {
                    'account_from': 1,
                    'account_to': 1,
                    'user': self.user1,
                    'created_at': today,
                    'amount': 10
                }
            )

    def test_money_transfer_serializer_create_account_not_exist(self):
        money_transfer = MoneyTransferSerializer()
        with self.assertRaises(NotFound):
            money_transfer.create(
                validated_data = {
                    'account_from': 1,
                    'account_to': 3,
                    'user': self.user1,
                    'created_at': today,
                    'amount': 10
                }
            )

    def test_money_transfer_serializer_create_negative_balance(self):
        money_transfer = MoneyTransferSerializer()
        with self.assertRaises(ValidationError):
            money_transfer.create(
                validated_data = {
                    'account_from': 1,
                    'account_to': 2,
                    'user': self.user1,
                    'created_at': today,
                    'amount': 101
                }
            )
