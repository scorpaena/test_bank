from django.contrib import admin
from .models import Account, MoneyTransferLog


class AccountAdmin(admin.ModelAdmin):
    list_display = ('account', 'currency', 'balance', 'created_at',)
    list_filter = ('account', 'currency', 'balance', 'created_at', )
    search_fields = ('account', 'currency', 'balance', 'created_at', )
    ordering = ('-created_at',)


class MoneyTransferLogAdmin(admin.ModelAdmin):
    list_display = ('account_from', 'account_to', 'created_at','amount')
    list_filter = ('account_from', 'account_to', 'created_at','amount')
    search_fields = ('account_from', 'account_to', 'created_at','amount')
    ordering = ('-created_at',)


admin.site.register(Account, AccountAdmin)
admin.site.register(MoneyTransferLog, MoneyTransferLogAdmin)
