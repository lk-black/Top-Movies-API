"""
Serializers para movie API views. 
"""
from rest_framework import serializers
from app.models import Movies


class MovieSerializer(serializers.ModelSerializer):
    """Serializer para o model movies API."""

    class Meta:
        model = Movies
        fields = ['id', 'name', 'description', 'rating', 'poster' , 'url' , 'datePublished', 'keywords', 'duration']
    
    
    def create(self, validated_data):
        """Cria um novo filme no banco de dados."""
        request = self.context.get('request')
        user = request.user
        return Movies.objects.create(**validated_data, user=user)
        
            
class ScraperMovieSerializer(serializers.Serializer):
    """Serializer para a lista de filmes encontrados."""
    
    name = serializers.CharField()
    url = serializers.CharField()
    poster = serializers.CharField()
    details = serializers.SerializerMethodField(method_name='get_details')

    def get_details(self, obj):
        """Método para criar um link que redireciona para os detalhes do filme."""
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/movies/scrape_movie_url/?url={obj["url"]}')
