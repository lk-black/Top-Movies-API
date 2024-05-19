"""
Serializers para movie API views. 
"""
from rest_framework import serializers
from app.models import Movies


class PersonalMovieListSerializer(serializers.ModelSerializer):
    """Serializer para o model movies API."""
    class Meta:
        fields = ('name','description', 'rating', 'datePublished', 'url', 'keywords', 'duration')
        model = Movies
        
        
class MoviesSerializer(serializers.Serializer):
    """Serializa a lista de filmes encontrados."""
    name = serializers.CharField()
    url = serializers.CharField()
    poster = serializers.CharField()
    details = serializers.SerializerMethodField(method_name='get_details')

    def get_details(self, obj):
        """Método para criar um link que redireciona para os detalhes do filme."""
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/movies/details/?url={obj["url"]}')
    
 
class DetailMovieSerializer(serializers.Serializer):    
    """Serializa os detalhes de um filme especifico."""
    name = serializers.CharField()
    description = serializers.CharField()
    rating = serializers.FloatField()
    url = serializers.CharField()
    poster = serializers.URLField()
    datePublished = serializers.DateField()
    keywords = serializers.CharField()
    duration = serializers.CharField()    
    add_to_db = serializers.SerializerMethodField()
    
    
    def create(self, validated_data):
        """Cria o modelo no banco de dados baseado no serializer."""
        return Movies.objects.create(**validated_data)

    
    def get_add_to_db(self, obj):
        """Adiciona o filme no banco de dados pela url."""
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/movies/add/?url={obj["url"]}')
