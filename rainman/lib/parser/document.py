"""
Document class for representing processed text and returning entities to client.
"""
from flask import jsonify

from entitycollection import EntityCollection

class Document(object):
    """
    Document object represents webpage, article, or other text, to be processed.
    """
    def __init__(self, title, text, domain):
        """
        Init from title, body text, and domain name.
        """
        self.title = title
        self.text = text
        self.domain = domain

        self.full_text = u"{title}\n{text}".format(title=self.title, text=self.text)

    def entities(self,verbose=False):
        """
        Fetches context info and returns final entities.
        """
        self._entities = EntityCollection(self.full_text)
        self._entities.fetch_info()
        self._entities.sort()
        self._entities.find_indices_in_text(self.full_text)
        if verbose:
            return self._entities.verbose()
        else:
            return self._entities.output()

    def news(self):
        """
        Fetches news articles related to the given document.
        """
        if not self._entities:
            self.entities()
        self._entities.fetch_news()
        return self._entities.news