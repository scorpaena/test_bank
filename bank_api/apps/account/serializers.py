from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound, ParseError
from django.core.exceptions import ObjectDoesNotExist
from .models import Account, MoneyTransferLog
from .exceptions import TransferValidationError, BalanceValidationError
from .services import money_transfer


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

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    account_from = serializers.PrimaryKeyRelatedField(
        queryset = Account.objects.all()
    )
    account_to = serializers.PrimaryKeyRelatedField(
        queryset = Account.objects.all()
    )
    amount = serializers.IntegerField(write_only=True)

    def validate(self, data):
        if data['user'].is_staff or data['user'] == data['account_from'].user: 
            return data
        else:
            raise serializers.ValidationError(
                '{} does not belong to {}'.format(data['account_from'], data['user'])
            )

    def create(self, validated_data):
        account_from = validated_data['account_from']
        account_to = validated_data['account_to']
        amount = validated_data['amount']
        try:
            money_transfer(account_from, account_to, amount)
        except ObjectDoesNotExist as error:
            raise NotFound (error)
        except TransferValidationError as error:
            raise ValidationError (error)
        except BalanceValidationError as error:
            raise ValidationError (error)
        else:
            return MoneyTransferLogSerializer().create(validated_data)


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
