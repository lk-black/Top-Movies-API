"""
Configuração de views para movie API. 
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .serializers import MoviesSerializer
from .movies import ScrapperIMBD




class ListMoviesView(APIView):
    """Lista os resultados do movie API."""
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='query',
                description='Busca por título de filme',
                required=True,
                type=str
            ),
        ],
        responses={200: MoviesSerializer(many=True)}
    )
    def get(self, request, format=None):
        """Faz uma busca pelo nome do filme e retorna os resultados."""
        query = request.query_params.get('query', '')
        if not query:
            return ValueError('Erro, o parâmetro query deve ser preenchido!')
        
        imdb = ScrapperIMBD()
        movies = imdb.search_by_name(query=query)
        serializer = MoviesSerializer(movies, many=True)
        return Response(serializer.data)