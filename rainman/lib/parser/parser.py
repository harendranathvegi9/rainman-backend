"""
Main Parser class for processing text and returning entities to client.
"""
from flask import jsonify

from ..alchemyapi import AlchemyAPI

# import nltk
# nltk.data.path.append('./nltk_data')

class Parser(object):
    def __init__(self, title, text, domain):
        self.title = title
        self.text = text
        self.domain = domain

        self.full_text = "{title}\n{text}".format(title=self.title, text=self.text)

    def parse(self, verbose=False):
        api = AlchemyAPI()
        return api.entities('text',self.full_text.encode('utf8'))