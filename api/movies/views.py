"""
Configuração de views para movie API. 
"""
from drf_spectacular.utils import extend_schema ,OpenApiParameter

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ScraperMovieSerializer, MovieSerializer
from .movies import ScrapperIMBD
from app.models import Movies

    
class MoviesAPIView(ModelViewSet):
    """ViewSet para movies API."""
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    
    def get_queryset(self):
        """Filtra os resultados dos filmes no banco de dados para serem respectivos ao usuário logado."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='url',
                description='URL do filme a ser adicionado.',
                required=True,
                type=str
            ),
        ],
        responses={201: 'Filme adicionado com sucesso', 400: 'Erro nos parâmetros',
                   409: 'Filme já existe', 401: 'Usuário não autorizado.'}
    )    
    def create(self, request, *args, **kwargs):
        """Cria e retorna um novo filme pela sua URL do IMDB."""
        url = request.query_params.get('url', '')
        if Movies.objects.filter(url=url).exists():
            return Response({'error': 'Filme já existe no banco de dados'}, status=status.HTTP_409_CONFLICT)
        
        imdb = ScrapperIMBD()
        movie_details = imdb.get(url=url)
        
        serializer = MovieSerializer(data=movie_details, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
        
    
    @extend_schema(
    parameters=[
        OpenApiParameter(
            name='query',
            description='Busca por título de filme',
            required=True,
            type=str
        ),
    ],
    responses={200: ScraperMovieSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_name='scrape-movies-name')
    def scrape_movies_name(self, request):
        """Lista os filmes raspados do IMDB com base no nome fornecido."""
        query = request.query_params.get('query', '')
        
        if not query:
            return ValueError('Erro, o parâmetro query deve ser preenchido!')
        
        imdb = ScrapperIMBD()
        movies = imdb.search_by_name(query=query)
        serializer = ScraperMovieSerializer(movies, many=True, context={"request": request})
        return Response(serializer.data)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='url',
                description='Busca pelo url do filme.',
                required=True,
                type=str
            ),
        ],
        responses={200: ScraperMovieSerializer},
    )
    @action(detail=False, methods=['get', 'post'])
    def scrape_movie_url(self, request):
        """Lista os detalhes do filme pela URL."""
        url = request.query_params.get('url', '')
        if not url:
            return Response({'error': 'Erro, o parâmetro url deve ser preenchido!'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        imdb = ScrapperIMBD()
        movie_details = imdb.get(url=url)
        serializer = self.serializer_class(movie_details, context={"request": request})
        return Response(serializer.data)