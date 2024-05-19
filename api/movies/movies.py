"""
Raspagem e coleta de filmes para o movie API. 
"""
from requests_html import HTMLSession
import json
from .utils import ImdbParser


class ScrapperIMBD:
    """Classe responsável por fazer a raspagem de Filmes no IMDB."""
    
    def __init__(self):
        """Inicia uma sessão HTML."""
        
        self.session = HTMLSession()
        self.headers = {
           "Accept": "application/json, text/plain, */*",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
           "Referer": "https://www.imdb.com/"
           }
        self.baseURL = "https://www.imdb.com"
        
    def search_by_name(self, query):
        """Faz a busca dos filmes, adiciona em uma lista, e retorna os resultados."""
        
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
        """Faz a requisição do filme pela url e retorna um JSON com todos os detalhes."""
        
        try:
            response = self.session.get(url)
            result = response.html.xpath("//script[@type='application/ld+json']")[0].text
            result = ''.join(result.splitlines())
            result = f"""{result}"""
        except IndexError:
            return self.NA
        
        try:
            result = json.loads(result)
        except json.decoder.JSONDecodeError as e:
            try:
                to_parse = ImdbParser(result)
                parsed = to_parse.remove_trailer
                parsed = to_parse.remove_description
                result = json.loads(parsed)
            except json.decoder.JSONDecodeError as e:
                try:
                    parsed = to_parse.remove_review_body
                    result = json.loads(parsed)
                except json.decoder.JSONDecodeError as e:
                    return self.NA

        output = {
            "name": result.get('name'),
            "url": self.baseURL + result.get('url').split("/title")[-1],
            "poster": result.get('image'),
            "description": result.get('description'),
            "rating": result.get("aggregateRating", {"ratingValue": None}).get("ratingValue"),
            "datePublished": result.get("datePublished"),
            "keywords": result.get("keywords"),
            "duration": result.get("duration"),
        }
        
        return output
