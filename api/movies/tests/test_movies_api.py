"""
Teste para recursos mo movie API. 
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from app.models import Movies
from movies.serializers import MovieSerializer


MOVIE_PERSONAL_LIST_URL = 'http://127.0.0.1:8000/api/movies/'

URL_FOR_MOVIES_TEST = 'https://www.imdb.com/title/tt15398776/?ref_=nv_sr_srsg_0_tt_3_nm_5_q_openhaime'
URL_FOR_MOVIES_TEST2 = 'https://www.imdb.com/title/tt0133093/?ref_=nv_sr_srsg_0_tt_8_nm_0_q_matrix'


def create_scrape_movies_list_by_name_url(name):
    """Cria e retorna a url para scrape-movies API."""
    return 'http://127.0.0.1:8000/api/movies/scrape_movies_name/?query=' + f'{name}/'

def create_scrape_detail_movie_url(url):
    """Cria e retorna os detalhes do filme pela url"""
    return 'http://127.0.0.1:8000/api/movies/scrape_movie_url/?url=' + f'{url}/'

def create_add_post_url(url):
    """Cria e retorna novo filme pela url."""
    return 'http://127.0.0.1:8000/api/movies/?url=' + f'{url}/'

def create_detail_id_movie_url(movie_id):
    """Cria e retorna a url para requisitar detalhes de um filme no banco de dados pelo id."""
    return ('http://127.0.0.1:8000/api/movies/' + f'{movie_id}/' )

def create_user(**params):
        """Cria e retorna um novo usuário."""
        return get_user_model().objects.create_user(**params)


class MoviesScraperAPITest(TestCase):
    """Testes para o movies scraper API."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='testuser@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)
        
    def test_movie_scraper_get_by_name_successful(self):
        """Testa os filmes estão sendo listados de acordo com o nome. """
        url = create_scrape_movies_list_by_name_url(name='batman')
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_movie_scraper_add_by_url(self):
        """Testa se o filme está sendo adicionado no banco de dados de acordo com a url fornecida."""
        url = create_add_post_url(
            url='https://www.imdb.com/title/tt15398776/?ref_=nv_sr_srsg_0_tt_3_nm_5_q_openhaime')
        res = self.client.post(url, user=self.user)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        movie  = Movies.objects.get()
        self.assertEqual(movie.user, self.user)
        self.assertEqual(movie.name, 'Oppenheimer')
    
        
class MoviesPersonalListTest(TestCase):
    """Testes para o personal list movies API."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='testuser@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(self.user)
    
    def test_retrieve_list_movies_db(self):
        """Testa se os filmes estão sendo listados corretamente."""
        url = create_add_post_url(url=URL_FOR_MOVIES_TEST)
        url2 = create_add_post_url(url=URL_FOR_MOVIES_TEST2)
        self.client.post(url, user=self.user)
        self.client.post(url2, user=self.user)
        
        res = self.client.get(MOVIE_PERSONAL_LIST_URL)
        movies = Movies.objects.all().order_by('-id')
        serializer = MovieSerializer(movies, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_retrieve_movie_detail(self):
        """Testa a requisição para os detalhes de um filme."""
        url_movie = create_add_post_url(URL_FOR_MOVIES_TEST2)
        
        self.client.post(url_movie, user=self.user)
        
        movie  = Movies.objects.get()
        url = create_detail_id_movie_url(movie.id)
        res = self.client.get(url)
        
        serializer = MovieSerializer(movie)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_partial_movie_update(self):
        """Testa a atualização parcial dos dados de um filme."""
        url_movie = create_add_post_url(URL_FOR_MOVIES_TEST2)
        self.client.post(url_movie, user=self.user)
        movie  = Movies.objects.get()
        url = create_detail_id_movie_url(movie.id)
        
        payload = {'name': 'new name'}
        res = self.client.patch(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        movie.refresh_from_db()
        self.assertEqual(movie.name, payload['name'])
        self.assertEqual(movie.user, self.user)

    def test_full_movie_update(self):
        """Testa a atualização total dos dados de um filme."""
        url_movie = create_add_post_url(URL_FOR_MOVIES_TEST2)
        self.client.post(url_movie, user=self.user)
        movie  = Movies.objects.get()
        
        url = create_detail_id_movie_url(movie_id=movie.id)
        
        request_details_url = create_scrape_detail_movie_url(
            url='https://www.imdb.com/title/tt0468569/?ref_=ls_t_1')
        
        movie_details = self.client.get(request_details_url)
        
        self.assertEqual(movie_details.status_code, status.HTTP_200_OK)

        payload = movie_details.json()
        res = self.client.put(url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        movie.refresh_from_db()        
        self.assertEqual(movie.name, payload['name'])
        self.assertEqual(movie.user, self.user)
    
    def test_delete_movie(self):
        """Testa se o filme foi deletado com sucesso."""
        url_movie = create_add_post_url(URL_FOR_MOVIES_TEST2)
        res = self.client.post(url_movie, user=self.user)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        movie  = Movies.objects.get()
        
        url = create_detail_id_movie_url(movie.id)
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movies.objects.filter(id=movie.id).exists())
        