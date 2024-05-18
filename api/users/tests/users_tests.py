"""
Testes para Users API. 
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

CREATE_USER_URL = reverse('users:create')


def create_user(**params):
    """Cria e retorna um novo usuário."""
    return get_user_model().objects.create_user(**params)


class PublicAPITest(TestCase):
    """Testa recursos públicos do user API."""
    
    def setUp(self):
        self.client = APIClient()
        
    def test_create_user_success(self):
        """Testa se o usuário está sendo criado com sucesso."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpassword123',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_email_with_exist_error(self):
            """Testa se um erro é retornado se o email cadastrado já existe."""
            payload = {
                'email': 'test@example.com',
                'password': 'testpassword123',
            }
            create_user(**payload)
            res = self.client.post(CREATE_USER_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_bad_credentials(self):
        """Testa se um erro é retornado ao usuário cadastrar uma senha muito curta."""
        payload = {
            'email': 'test@example.com',
            'password': 'tw',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertNotEqual(res.status_code, status.HTTP_201_CREATED)
        