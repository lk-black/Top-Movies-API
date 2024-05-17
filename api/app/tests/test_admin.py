"""
Tests para model admin. 
"""
from django.test import TestCase, Client 
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

class TestAdminSite(TestCase):
    """Teste para recursos do User Admin Model."""
    def setUp(self):
        """Criação do user e client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='testpassword123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='userpassword123',
            first_name='Test',
            last_name='User',
        )
    
    def test_user_list(self):
        """Test para conferir se a pagina edit está funcionando."""
        url = reverse('admin:app_user_changelist')
        
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)   
    