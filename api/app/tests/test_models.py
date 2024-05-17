"""
Teste para modelos do banco de dados.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """Testes para models."""
    def test_user_create_successful(self):
        """Teste para conferir se o Custom User Model está sendo criado com sucesso."""
        email = 'test@test.com'
        password = 'testpassword123'
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpassword123',
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password)) 
        
    def test_normalize_email(self):
        """Testa o método normalize_email"""
        emails = [
            ['test@EXAMPLE.com', 'test@example.com'],
            ['Test2@Example.Com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
        ]
        
        for email, expected in emails:
            user = get_user_model().objects.create_user(email=email,
                                                        password='password123')
            self.assertEqual(user.email, expected)
            
    def test_email_input_required_validate(self):
        """Testa se o email está sendo requerido."""
        with(self.assertRaises(ValueError)):
            user = get_user_model().objects.create_user(
            email='',
            password='password123',
        )
    
    
    def test_create_super_user(self):
        """Testa se o superuser está sendo criado corretamente."""
        email = 'superuser@examplo.com'
        password = 'superuser123'
        superuser = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)