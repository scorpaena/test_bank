from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound, ParseError
from django.core.exceptions import ObjectDoesNotExist
from .models import Account, MoneyTransferLog
from .exceptions import TransferValidationError, BalanceValidationError
from .services import (
    money_transfer,
    to_money_transfer_log
)


class AccountCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            'account',
            'currency',
            'balance',
            'created_at',
            'user',
        ]
        read_only_fields = ['currency',]


class AccountDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = [
            'account',
            'currency',
            'balance',
            'created_at',
            'user',
        ]


class MoneyTransferSerializer(serializers.Serializer):
   
    account_from = serializers.IntegerField(write_only=True)
    account_to = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        account_from = validated_data['account_from']
        account_to = validated_data['account_to']
        user = validated_data['user']
        amount = validated_data['amount']
        try:
            money_transfer(account_from, account_to, amount)
        except ObjectDoesNotExist:
            raise NotFound ('double check if account from/to exists')
        except TransferValidationError:
            raise ValidationError ('account from/to must be different')
        except BalanceValidationError:
            raise ValidationError ('you don not have enough money')
        else:
            return to_money_transfer_log(account_from, account_to, user, amount)


class MoneyTransferLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MoneyTransferLog
        fields = [
            'account_from',
            'account_to',
            'user',
            'created_at',
            'amount',
        ]
