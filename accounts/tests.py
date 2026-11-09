from django.contrib.auth import get_user_model
from django.core.checks import Tags, run_checks
from django.test import SimpleTestCase
from django.urls import Resolver404, resolve
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationLoginTests(APITestCase):
    def test_registered_user_can_log_in_immediately(self):
        credentials = {
            'username': 'registration_login_test',
            'password': 'Registration-Test-927!',
        }
        response = self.client.post('/api/register/', {
            **credentials,
            'email': 'registration@example.com',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=credentials['username'])
        self.assertTrue(user.check_password(credentials['password']))

        response = self.client.post('/api/token/', credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class UserModelTests(SimpleTestCase):
    def test_builtin_user_model_has_no_reverse_accessor_clashes(self):
        self.assertEqual(get_user_model()._meta.label, 'auth.User')
        clashes = [
            error for error in run_checks(tags=[Tags.models])
            if error.id == 'fields.E304'
        ]
        self.assertEqual(clashes, [])


class AuthenticationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = 'Example-Account-Password-927!'
        cls.user = get_user_model().objects.create_user(
            username='accountuser',
            email='account@example.com',
            password=cls.password,
        )

    def login(self):
        response = self.client.post('/auth/jwt/create/', {
            'username': self.user.username,
            'password': self.password,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        return response.data

    def test_registration(self):
        response = self.client.post('/auth/users/', {
            'username': 'newaccount',
            'email': 'new@example.com',
            'password': self.password,
            'first_name': 'New',
            'last_name': 'Account',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)
        user = get_user_model().objects.get(username='newaccount')
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'Account')

    def test_registration_rejects_weak_password(self):
        response = self.client.post('/auth/users/', {
            'username': 'newaccount',
            'password': '123',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertFalse(get_user_model().objects.filter(username='newaccount').exists())

    def test_current_user_requires_authentication(self):
        response = self.client.get('/auth/users/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_and_current_user(self):
        tokens = self.login()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get('/auth/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertNotIn('password', response.data)

    def test_login_rejects_wrong_password(self):
        response = self.client.post('/auth/jwt/create/', {
            'username': self.user.username,
            'password': 'wrong-password',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_and_verify(self):
        tokens = self.login()
        response = self.client.post('/auth/jwt/refresh/', {
            'refresh': tokens['refresh'],
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access = response.data['access']
        response = self.client.post('/auth/jwt/verify/', {
            'token': access,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(
            self.client.get('/auth/users/me/').status_code,
            status.HTTP_200_OK,
        )

    def test_invalid_tokens_are_rejected(self):
        for endpoint, field in [('verify', 'token'), ('refresh', 'refresh')]:
            with self.subTest(endpoint=endpoint):
                response = self.client.post(f'/auth/jwt/{endpoint}/', {
                    field: 'invalid-token',
                }, format='json')
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_current_user_can_update_names(self):
        tokens = self.login()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.patch('/auth/users/me/', {
            'first_name': 'Updated',
            'last_name': 'Name',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')

    def test_legacy_token_login_is_not_exposed(self):
        with self.assertRaises(Resolver404):
            resolve('/auth/token/login/')
