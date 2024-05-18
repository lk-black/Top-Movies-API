"""
Serializers para user API.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


class UserSerializer(serializers.ModelSerializer):
    """Serializer para o user object."""
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name']
        
    def create(self, validate_data):
        """Cria e retorna um usuário com a senha criptografada."""
        return get_user_model().objects.create_user(**validate_data)
    

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        """Faz a validação e autenticação do usuário."""
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = 'Insira credenciais para poder se autenticar'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
    