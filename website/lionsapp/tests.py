from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse

# Create your tests here.
class LoginTests(TestCase):

    def test_login(self):
        client = Client()
        response = client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
