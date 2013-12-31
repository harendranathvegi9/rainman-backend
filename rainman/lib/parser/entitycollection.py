"""
Classes representing each type of Named Entity, and a collection of Named Entities.
"""
import gevent
from gevent import monkey
monkey.patch_all(thread=False) # patches all calls to Socket in any modules following this line

from ..alchemyapi import AlchemyAPI
from ..bingapi import BingAPI
from ..freebaseapi import FreebaseAPI

class EntityCollection(object):
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
        Extract entities from the given text with the AlchemyAPI.
        """
        api = AlchemyAPI()
        api_entities = api.entities('text',text.encode('utf8'))['entities']
        self._entities = [Entity(api_entity) for api_entity in api_entities]

    def find_indices_in_text(self, text):
        """
        Finds the indices in the given text for all entities.
        """
        def _find_all(str, sub):
            "Return indices for all sub matches in str"
            start = 0
            while True:
                start = str.find(sub, start)
                if start == -1: return
                yield start
                start += len(sub)

        def _pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            from itertools import izip, tee
            a, b = tee(iterable)
            next(b, None)
            return izip(a, b)

        def _overlap(tuples, tuple):
            "True if index range of tuple overlaps with member of tuples"
            t = list(tuples)
            t.append(tuple)
            t.sort()
            for tuple1, tuple2 in _pairwise(t):
                if tuple1[1] >= tuple2[0]:
                    return True
            return False

        all_indices = []
        for entity in self._entities:
            term = entity.text
            length = len(term)
            for index in _find_all(text, term):
                indices = (index, index+length)
                if not _overlap(all_indices, indices):
                    all_indices.append(indices)
                    entity.indices.append(indices)

    def fetch_info(self):
        """
        Fetch info for each entity in collection.
        """
        
        jobs = [gevent.spawn(entity.fetch_info) for entity in self._entities]
        gevent.joinall(jobs, timeout=5)

    def fetch_news(self):
        """
        Fetch news stories related to the set of entities in this collection
        """
        query_str = " ".join([entity.text for entity in self._entities])
        api = BingAPI()
        self.news = api.news(query_str)

    def sort(self):
        """
        Sort the entities in order of most relevant
        to least relevant.
        """
        for entity in self._entities:
            if not entity.disambiguated:
                entity.relevance /= 2
        self._entities.sort(key=lambda e: e.relevance, reverse=True)

    def verbose(self):
        """
        Return a list of verbose output from each entity.
        """
        return [entity.verbose() for entity in self._entities]

    def output(self):
        """
        Return a list of output from each entity.
        """
        return [entity.output() for entity in self._entities if entity.disambiguated]


class Entity(object):
    """
    Python object representing Named Entity.
    """
    def __init__(self, api_entity):
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
            self.disambiguated = None
            pass

        self.description = None
        self.image_url = None

        # list of indice tuples
        self.indices = []

    # def fetch_news(self):
    #     """
    #     Fetches news stories about this entity from Bing news API.
    #     """
    #     api = BingAPI()
    #     self.news_stories = api.news(self.text)

    # def fetch_image(self):
    #     """
    #     Fetches images about this entity from Bing news API.
    #     """
    #     api = BingAPI()
    #     self.images = api.image(self.text)

    @property
    def _freebase_mid(self):
        """
        Property of the Freebase MQL ID of the entity, or None
        if the entity was not disambiguated by Alchemy.
        """
        try:
            freebase_url = self.disambiguated['freebase']
            mid_frag = freebase_url.rpartition('/')[-2:]
            mid = "".join(mid_frag).replace('.','/')
            return mid
        except:
            return None

    def fetch_info(self):
        """
        Method to fetch info from external service.
        """
        if not self._freebase_mid:
            return
        api = FreebaseAPI(self._freebase_mid)
        self.description = api.description()
        self.image_url = api.image_url()

    def output(self):
        """
        Default output returns just Named Entity name & type.
        """
        return {
            'text': self.text,
            'type': self.type,
            'description': self.description,
            'image_url': self.image_url,
            'indices': self.indices
        }

    def verbose(self):
        """
        Verbose output returns extra information for admin view.
        """
        return {
            'text': self.text,
            'type': self.type,
            'relevance': self.relevance,
            'count': self.count,
            'disambiguated': self.disambiguated,
            'mid': self._freebase_mid,
            'description': self.description,
            'image_url': self.image_url,
            'indices': self.indices
        }