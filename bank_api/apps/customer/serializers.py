from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        max_length=128, write_only=True, style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        max_length=128, write_only=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password1', 'password2']

    def create(self, validated_data):
        password1 = validated_data.pop('password1', '')
        password2 = validated_data.pop('password2', '')
        try:
            validate_password(password1, self.instance)
        except DjangoValidationError as error:
            raise ValidationError (error)
        if password1 and password2 and password1 != password2:
            raise ValidationError ('password mismatch')
        return User.objects.create_user(password=password1, **validated_data)


class AuthenticationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, 
        write_only=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['username', 'password']
