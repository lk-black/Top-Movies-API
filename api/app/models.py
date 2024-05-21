"""
Modelos do banco de dados.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class ManagerUser(BaseUserManager):
    """Gerenciamento de usuários."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Cria, salva, e retorna um novo usuário."""
        if not email:
            raise ValueError('Usuário deve inserir um endereço de E-mail')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None):
        """Cria, salva, e retorna um novo superuser."""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user
    

class User(AbstractUser):
    """Usuário do sistema"""
    
    username = None
    email = models.EmailField(unique=True)
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    
    objects = ManagerUser()
    
    def __str__(self):
        return self.email


class Movies(models.Model):
    """Modelo de banco de dados para movies API."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    poster = models.URLField(null=True, blank=True)
    description = models.TextField(default='N/A', blank=True, null=True)
    rating = models.FloatField(default=1.0)
    datePublished = models.DateField()
    keywords = models.CharField(null=True, blank=True)
    duration = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.name
