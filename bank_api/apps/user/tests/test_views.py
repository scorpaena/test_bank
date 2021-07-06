from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    
    def setUp(self):
        self.client_user = APIClient()
       
        self.user = User.objects.create_user(
            username = 'foo', 
            password = 'bar'
            )

    def test_user_login(self):
        request = self.client_user.post('/user/login/',
            data = {
                'username': 'foo', 
                'password': 'bar'
            }
        )
        self.assertEqual(request.status_code, 200)
    
    def test_user_login_wrong_passw(self):
        request = self.client_user.post('/user/login/',
            data = {
                'username': 'foo', 
                'password': 'bar1'
            }
        )
        self.assertEqual(request.status_code, 403)

    def test_user_login_wrong_username(self):
        request = self.client_user.post('/user/login/',
            data = {
                'username': 'foo1', 
                'password': 'bar'
            }
        )
        self.assertEqual(request.status_code, 403)

    def test_user_logout(self):
        response = self.client_user.get('/user/logout/',)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),'you are logged out')

