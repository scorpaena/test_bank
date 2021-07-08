from django.urls import path
from .views import (
    AccountListCreateView,
    AccountDetailView,
    MoneyTransferView,
    MoneyTransferAllLogView,
    MoneyTransferAccountLogView,
)

urlpatterns = [
    path("create_account/", AccountListCreateView.as_view()),
    path("<int:pk>/", AccountDetailView.as_view()),
    path("money_transfer/", MoneyTransferView.as_view()),
    path("transfer_log/", MoneyTransferAllLogView.as_view()),
    path("transfer_log/<int:account_from>/", MoneyTransferAccountLogView.as_view()),
]
