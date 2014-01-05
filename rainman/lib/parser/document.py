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
        self._entities.find_indices_in_text(self.text)
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

    # html for entities now inserted on frontend
    #
    # def html(self):
    #     if not self._entities:
    #         self.entities()
    #     output = self.text
    #     all = []
    #     for i, entity in enumerate(self._entities.output()):
    #         for indices in entity['indices']:
    #             elt = {}
    #             elt['indices'] = indices
    #             elt['i'] = i+1
    #             elt['text'] = entity['text']
    #             all.append(elt)
    #     all.sort(key=lambda e: e['indices'][0])
    #     offset = 0
    #     for elt in all:
    #         start = offset + elt['indices'][0]
    #         end = offset + elt['indices'][1]
    #         original = output[start:end]
    #         sub = u'<span class="entity">{0}<span data-index="{1}" class="index">{1}</span></span>'.format(original, elt['i'])
    #         output = "".join([output[:start],sub,output[end:]])
    #         offset += len(sub) - len(original)
    #     return output