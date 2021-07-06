from django.test import TestCase
from rest_framework.exceptions import ValidationError
from apps.user.serializers import UserSignUpSerializer


class UserSerializerTestCase(TestCase):
    
    def test_user_signup(self):
        user_signup = UserSignUpSerializer(
            data = {
            'username': 'foo', 
            'password1': 'bar123$%',
            'password2': 'bar123$%',
            }
        )
        self.assertTrue(user_signup.is_valid())
    
    def test_user_signup_invalid_data(self):
        user_signup = UserSignUpSerializer(
            data = {
                'username': '', 
                'password1': 'bar',
                'password2': 'bar',
            }
        )
        self.assertFalse(user_signup.is_valid())

    def test_user_signup_create(self):
        user_signup = UserSignUpSerializer()
        user_signup.create(
            validated_data = {
                'username': 'foo', 
                'password1': 'bar123$%',
                'password2': 'bar123$%',
            }
        )

    def test_user_signup_create_passw_mismatch(self):
        user_signup = UserSignUpSerializer()
        with self.assertRaises(ValidationError):
            user_signup.create(
                validated_data = {
                'username': 'foo', 
                'password1': 'bar123$%',
                'password2': 'bar123$',
                }
            )

    def test_user_signup_create_weak_passw(self):
        user_signup = UserSignUpSerializer()
        with self.assertRaises(ValidationError):
            user_signup.create(
                validated_data = {
                    'username': 'foo', 
                    'password1': 'bar',
                    'password2': 'bar',
                }
            )
