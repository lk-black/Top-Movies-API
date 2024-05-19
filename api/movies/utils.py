"""
Faz a manipulação de strings json. 
"""


class ImdbParser:
    """Uma classe para manipular dados de string json recebidos de um filme/TV do IMDB."""
    
    def __init__(self, json_string):
        self.json_string = json_string

    @property
    def remove_trailer(self):
        """Ajuda a remover o schema 'trailer' da string da string json de dados do IMDB."""
        
        try:
            self.json_string = ''.join(self.json_string.splitlines())
            trailer_i = self.json_string.index('"trailer"')
            actor_i = self.json_string.index('"actor"')
            to_remove = self.json_string[trailer_i:actor_i:1]
            self.json_string = self.json_string.replace(to_remove, "")
        except ValueError:
            self.json_string = self.json_string
        return self.json_string

    @property
    def remove_description(self):
        """Ajuda a remover o esquema de 'descrição' da string json do arquivo IMDB."""
        
        try:
            review_i = self.json_string.index('"review"')
            des_i = self.json_string.index('"description"', 0, review_i)
            to_remove = self.json_string[des_i:review_i:1]
            self.json_string = self.json_string.replace(to_remove, "")
        except ValueError:
            self.json_string = self.json_string
        return self.json_string

    @property
    def remove_review_body(self):
        """Ajuda a remover o esquema 'reviewBody' da string json do arquivo IMDB."""
        
        try:
            reviewrating_i = self.json_string.index('"reviewRating"')
            reviewbody_i = self.json_string.index('"reviewBody"', 0, reviewrating_i)
            to_remove = self.json_string[reviewbody_i:reviewrating_i:1]
            self.json_string = self.json_string.replace(to_remove, "")
        except ValueError:
            self.json_string = self.json_string
        return self.json_string