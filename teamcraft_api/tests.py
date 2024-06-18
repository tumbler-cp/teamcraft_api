from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token


class AuthTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')
        self.token_url = reverse('token')
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'password123',
            'username': 'testuser'
        }

    def test_signup(self):
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_signin(self):
        self.client.post(self.signup_url, self.user_data, format='json')
        response = self.client.post(self.signin_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)

    def test_signin_wrong_password(self):
        self.client.post(self.signup_url, self.user_data, format='json')
        wrong_data = self.user_data.copy()
        wrong_data['password'] = 'wrongpassword'
        response = self.client.post(self.signin_url, wrong_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Not found')

    def test_token_auth(self):
        response = self.client.post(self.signup_url, self.user_data, format='json')
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(self.token_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Passed for', response.data)

    def test_token_auth_without_token(self):
        response = self.client.get(self.token_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
