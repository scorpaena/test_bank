from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from .serializers import UserSignUpSerializer, AuthenticationSerializer


class UserSignUpView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer


class Login(generics.CreateAPIView):
    serializer_class = AuthenticationSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            response = {"error": "username/password is wrong or user is disabled"}
            return Response(response, status=HTTP_403_FORBIDDEN)
        else:
            login(request, user)
            response = {"success": "you are logged in"}
            return Response(response, status=HTTP_200_OK)


def logout_view(request):
    logout(request)
    response = {"you are logged out"}
    return HttpResponse(response)
