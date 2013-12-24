"""
Classes representing each type of Named Entity, and a collection of Named Entities.
"""
from ..alchemyapi import AlchemyAPI

class Entities(object):
    """
    Collection of Entity options with group methods.
    """
    def __init__(self, text):
        """
        Upon instantiation, extract Named Entities from text
        """
        self._extract_from_text(text)

    def _extract_from_text(self, text):
        """
        Extract entities from the AlchemyAPI.
        """
        api = AlchemyAPI()
        api_entities = api.entities('text',text.encode('utf8'))['entities']
        self._entities = [Entity(api_entity) for api_entity in api_entities]

    def fetch_info(self):
        """
        Fetch info for each entity in collection.
        """
        for entity in self._entities:
            entity.fetch_info()

    def verbose(self):
        """
        Return a list of verbose output from each entity.
        """
        return [entity.verbose() for entity in self._entities]
    
    def output(self):
        """
        Return a list of output from each entity.
        """
        return [entity.output() for entity in self._entities]


class Entity(object):
    """
    Python object representing Named Entity.
    """
    def __init__(self, api_entity):
        """
        Init from dict returned by API
        """
        # original text match
        self.text = api_entity['text']
        # type of entity
        self.type = api_entity['type']
        # relevance score
        self.relevance = float(api_entity['relevance'])
        # count in article
        self.count = int(api_entity['count'])

        # info for disambiguity
        try:
            self.disambiguated = api_entity['disambiguated']
        except:
            pass
        # list of indice tuples
        # self.indices

    def fetch_info(self):
        """
        Method to fetch info from external service.
        """
        pass

    def output(self):
        """
        Default output returns just Named Entity name & type.
        """
        return {
            'text': self.text,
            'type': self.type
        }

    def verbose(self):
        """
        Verbose output returns extra information for admin view.
        """
        return {
            'text': self.text,
            'type': self.type,
            'relevance': self.relevance,
            'count': self.count
        }