from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Account, MoneyTransferLog
from .services import money_transfer, is_account_to_valid, to_money_transfer_log


class AccountCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['currency',]


class MoneyTransferSerializer(serializers.Serializer):
   
    account_from = serializers.HiddenField(default=None)
    account_to = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    account = serializers.ReadOnlyField()
    currency = serializers.ReadOnlyField()
    balance = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()

    def update(self, instance, validated_data):
        account_from = validated_data['account_from']
        account_to = validated_data['account_to']
        amount = validated_data['amount']
        if is_account_to_valid(account_from, account_to):
            money_transfer(account_from, account_to, amount)
            to_money_transfer_log(**validated_data)
        else:
            raise ValidationError ("'account_from' and 'account_to' must be different")
        return instance


class MoneyTransferLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MoneyTransferLog
        fields = '__all__'