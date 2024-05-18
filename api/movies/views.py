"""
Configuração de views para movie API. 
"""
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MoviesSerializer
from .movies import ScrapperIMBD


class ListMoviesView(APIView):
    """Lista os resultados do movie API."""
    
    def get(self, request, format=None):
        """Faz a busca pelo nome do file e retorna os resultados."""
        query = request.query_params.get('query', '')
        if not query:
            return ValueError('Erro, o parâmetro query deve ser preenchido!')
        
        imdb = ScrapperIMBD()
        movies = imdb.search_by_name(query=query)
        serializer = MoviesSerializer(movies, many=True)
        return Response(serializer.data)