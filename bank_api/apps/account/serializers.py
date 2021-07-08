from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound, ParseError
from django.core.exceptions import ObjectDoesNotExist
from .models import Account, MoneyTransferLog
from .exceptions import TransferValidationError, BalanceValidationError
from .services import money_transfer, to_money_transfer_log
from .validators import AccountFromToValidator, BalanceValidator


class AccountCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "account",
            "currency",
            "balance",
            "created_at",
            "user",
        ]
        read_only_fields = [
            "currency",
        ]


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "account",
            "currency",
            "balance",
            "created_at",
            "user",
        ]


class FilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        logged_in_user = self.context["request"].user
        if logged_in_user.is_staff:
            return Account.objects.all()
        else:
            return Account.objects.filter(user=logged_in_user)


class MoneyTransferSerializer(serializers.Serializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    account_from = FilteredPrimaryKeyRelatedField()
    account_to = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    amount = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        account_from = validated_data["account_from"]
        account_to = validated_data["account_to"]
        user = validated_data["user"]
        amount = validated_data["amount"]
        try:
            money_transfer(account_from, account_to, amount)
        except ObjectDoesNotExist as error:
            raise NotFound(error)
        except TransferValidationError as error:
            raise ValidationError(error)
        except BalanceValidationError as error:
            raise ValidationError(error)
        else:
            return to_money_transfer_log(account_from, account_to, user, amount)

    class Meta:
        validators = [
            AccountFromToValidator(),
            BalanceValidator(),
        ]


class MoneyTransferLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyTransferLog
        fields = [
            "account_from",
            "account_to",
            "user",
            "created_at",
            "amount",
        ]
