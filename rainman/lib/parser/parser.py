"""
Main Parser class for processing text and returning entities to client.
"""
from flask import jsonify

from ..alchemyapi import AlchemyAPI
from .entities import Entity

# import nltk
# nltk.data.path.append('./nltk_data')

class Parser(object):
    def __init__(self, title, text, domain):
        """
        Named entities are parsed upon class instantiation.
        """
        self.title = title
        self.text = text
        self.domain = domain

        self.full_text = u"{title}\n{text}".format(title=self.title, text=self.text)

        api = AlchemyAPI()
        api_entities = api.entities('text',self.full_text.encode('utf8'))['entities']
        
        self.entities = [Entity(e) for e in api_entities]

    def fetch_entities(self,verbose=False):
        """
        Fetches context info and returns final entities.
        """
        for entity in self.entities:
            entity.fetch_info()
        if verbose:
            output = [entity.verbose() for entity in self.entities]
        else:
            output = [entity.output() for entity in self.entities]
        return output