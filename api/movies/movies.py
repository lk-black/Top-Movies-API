"""
Raspagem e coleta de filmes para o movie API. 
"""
from requests_html import HTMLSession
import json


class ScrapperIMBD:
    """Raspa, lista, e detalha filmes do IMDB."""
    
    def __init__(self):
        """Inicia uma sessão HTML."""
        
        self.session = HTMLSession()
        self.headers = {
           "Accept": "application/json, text/plain, */*",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
           "Referer": "https://www.imdb.com/"
           }
        self.baseURL = "https://www.imdb.com"
        self.search_results = {'result_count': 0, 'results': []}
        
    def search_by_name(self, query):
        """Faz a busca dos filmes, lista, e retorna os resultados em JSON."""
        
        url = f"https://www.imdb.com/find?q={query}"
        response = self.session.get(url=url)
        results = response.html.xpath("//section[@data-testid='find-results-section-title']/div/ul/li")
        
        output = []
        for result in results:
            movie_name = result.text.replace('\n', ' ')
            url = result.find('a')[0].attrs['href']
            image = result.xpath("//img")[0].attrs['src']
            file_id = url.split('/')[2]
            
            output.append({
                'id': file_id,
                "name": movie_name,
                "url": f"https://www.imdb.com{url}",
                "poster": image
                })
            
            movies_result = output
        return movies_result
    
    def get(self, url):
        """Requisita os detalhes do filme pela URL e retorna os resultados em JSON"""
        ...