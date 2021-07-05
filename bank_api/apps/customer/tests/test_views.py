from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    
    def setUp(self):
        self.client_customer = APIClient()

        self.credentials_payload = {
            'username': 'foo', 
            'password': 'bar'
        }

        self.credentials_payload_wrong_passw = {
            'username': 'foo', 
            'password': 'bar1'
        }

        self.credentials_payload_wrong_username = {
            'username': 'foo1', 
            'password': 'bar'
        }
        
        self.customer = User.objects.create_user(**self.credentials_payload)


    def test_customer_login(self):
        request = self.client_customer.post('/customer/login/',
            data = self.credentials_payload
        )
        self.assertEqual(request.status_code, 200)
    
    def test_customer_login_wrong_passw(self):
        request = self.client_customer.post('/customer/login/',
            data = self.credentials_payload_wrong_passw
        )
        self.assertEqual(request.status_code, 403)

    def test_customer_login_wrong_username(self):
        request = self.client_customer.post('/customer/login/',
            data = self.credentials_payload_wrong_username
        )
        self.assertEqual(request.status_code, 403)

    def test_customer_logout(self):
        response = self.client_customer.get('/customer/logout/',)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),'you are logged out')

