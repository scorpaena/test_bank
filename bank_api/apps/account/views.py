from rest_framework import generics
from .models import Account, MoneyTransferLog
from .serializers import (
    AccountCreationSerializer,
    AccountDetailSerializer,
    MoneyTransferSerializer,
    MoneyTransferLogSerializer
)


class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountCreationSerializer


class AccountDetailView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializer


class MoneyTransferView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = MoneyTransferSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MoneyTransferAllLogView(generics.ListAPIView):
    queryset = MoneyTransferLog.objects.all()
    serializer_class = MoneyTransferLogSerializer


class MoneyTransferAccountLogView(generics.ListAPIView):
    queryset = MoneyTransferLog.objects.all()
    serializer_class = MoneyTransferLogSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            account_from=self.kwargs.get('account_from'), 
        )
