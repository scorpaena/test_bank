from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Account, MoneyTransferLog
from .serializers import (
    AccountCreationSerializer, 
    MoneyTransferSerializer, 
    MoneyTransferLogSerializer
)


class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountCreationSerializer
    permission_classes = [IsAdminUser,]


class AccountDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MoneyTransferSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        self.queryset = Account.objects.all()
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(customer=self.request.user)

    def perform_update(self, serializer):
        serializer.save(
            account_from=self.get_object(),
            customer=self.request.user
        )


class MoneyTransferCustomerLogView(generics.ListAPIView):
    serializer_class = MoneyTransferLogSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        self.queryset = MoneyTransferLog.objects.all()
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(customer=self.request.user)


class MoneyTransferAccountLogView(generics.ListAPIView):
    serializer_class = MoneyTransferLogSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        self.queryset = MoneyTransferLog.objects.all().filter(
            account_from=self.kwargs.get('account_from')
        )
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(account_from__customer=self.request.user)
