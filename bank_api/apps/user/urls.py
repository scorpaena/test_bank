from django.urls import path
from .views import UserSignUpView, Login, logout_view

urlpatterns = [
    path('signup/', UserSignUpView.as_view()),
    path('login/', Login.as_view()),
    path('logout/', logout_view),
]