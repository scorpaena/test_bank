from rest_framework.exceptions import ValidationError


class AccountFromToValidator:
    def __call__(self, attrs):
        if attrs["account_from"] == attrs["account_to"]:
            raise ValidationError("accounts must be different")


class BalanceValidator:
    def __call__(self, attrs):
        if attrs["account_from"].balance < attrs["amount"]:
            raise ValidationError("not enough money")
