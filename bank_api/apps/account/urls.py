from django.urls import path
from .views import (
    AccountListCreateView,
    AccountDetailView,
    MoneyTransferCustomerLogView,
    MoneyTransferAccountLogView
)

urlpatterns = [
    path('create_account/', AccountListCreateView.as_view()),
    path('<int:pk>/', AccountDetailView.as_view()),
    path('transfer_log/', MoneyTransferCustomerLogView.as_view()),
    path('transfer_log/<int:account_from>/', MoneyTransferAccountLogView.as_view()),
]