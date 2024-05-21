"""
Configuração de views para movie API. 
"""
from drf_spectacular.utils import extend_schema ,OpenApiParameter
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListCreateAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import MoviesSerializer, PersonalMovieListSerializer, DetailMovieSerializer
from .movies import ScrapperIMBD
from app.models import Movies


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
        """Função responsável por fazer a busca no site IMDB e listar os resultados."""
        
        query = request.query_params.get('query', '')
        if not query:
            return ValueError('Erro, o parâmetro query deve ser preenchido!')
        
        imdb = ScrapperIMBD()
        movies = imdb.search_by_name(query=query)
        serializer = MoviesSerializer(movies, many=True, context={"request": request})
        return Response(serializer.data)


class DetailMovieView(CreateAPIView):
    """Lista os detalhes do filme pela URL."""
    queryset = Movies.objects.all()
    serializer_class = DetailMovieSerializer
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='url',
                description='Busca pelo url do filme.',
                required=True,
                type=str
            ),
        ],
        responses={200: DetailMovieSerializer},
    )
    def get(self, request, format=None):
        """Função responsável por fazer o scraper do filme pela URL do IMDB e listar os detalhes."""
        
        url = request.query_params.get('url', '')
        if not url:
            return Response({'error': 'Erro, o parâmetro url deve ser preenchido!'}, status=status.HTTP_400_BAD_REQUEST)
        
        imdb = ScrapperIMBD()
        movie_details = imdb.get(url=url)
        serializer = DetailMovieSerializer(movie_details, context={"request": request})
        return Response(serializer.data)
    

class AddMovieView(ListCreateAPIView):
    """Adiciona o filme ao banco de dados."""
    queryset = Movies.objects.all()
    serializer_class = PersonalMovieListSerializer
    
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
    def post(self, request, format=None):
        """Cria e salva o filme pela url no banco de dados."""
        
        url = request.query_params.get('url', '')
        if not url:
            return Response({'error': 'Erro, o parâmetro url deve ser preenchido!'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Movies.objects.filter(url=url).exists():
            return Response({'error': 'Filme já existe no banco de dados'}, status=status.HTTP_409_CONFLICT)
        
        imdb = ScrapperIMBD()
        movie_details = imdb.get(url=url)
        if not movie_details:
            return Response({'error': 'Filme não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_authenticated:
            return Response({'error': 'Usuário não registrado'}, status=status.HTTP_401_UNAUTHORIZED)

        movie = Movies(
            user = request.user,
            name=movie_details['name'],
            url=movie_details['url'],
            poster=movie_details['poster'],
            description=movie_details['description'],
            rating=movie_details['rating'],
            datePublished=movie_details['datePublished'],
            keywords=movie_details['keywords'],
            duration=movie_details['duration'],
        )
        movie.save()
        
        return Response({'success': 'Filme adicionado com sucesso'}, status=status.HTTP_201_CREATED)


class PersonalMovieListView(ModelViewSet):
    """Viewset para os filmes que estão no banco de dados."""
    queryset = Movies.objects.all()
    serializer_class = PersonalMovieListSerializer
    
    def get_queryset(self):
        """Filtra os resultados dos filmes no banco de dados para serem respectivos ao usuário logado."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
    