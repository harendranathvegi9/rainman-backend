"""
Main Parser class for stripping text, title, and author from article HTML
"""
from flask import jsonify, current_app

from readability.readability import Document
import wikipedia

from collections import defaultdict
import json
import simplejson

import nltk

nltk.data.path.append('./nltk_data')

class Parser:
    def __init__(self, title, text, domain):
        self.title = title
        self.text = text
        self.domain = domain
        
        self.sentences = None
        self.words = None
        self.tagged = None
        self.ners = None

        self._ne = []
        self._ne_count = defaultdict(int)

    def sent_tokenize(self):
        self.sentences = nltk.sent_tokenize(self.text.encode('utf-8'))
        return self.sentences

    def word_tokenize(self):
        if not self.sentences:
            self.sent_tokenize()
        self.words = [nltk.word_tokenize(sent) for sent in self.sentences]
        return self.words

    def tag(self):
        if not self.words:
            self.word_tokenize()
        self.tagged = [nltk.pos_tag(word) for word in self.words]
        return self.tagged

    def ner(self):
        if not self.tagged:
            self.tag()
        trees = nltk.batch_ne_chunk(self.tagged)
        for tree in trees:
            self._ner_traverse(tree)
        self._ne.sort(key=lambda x: self._ne_count[str(x)], reverse=True)

        terms = []
        for ne in self._ne:
            term = ""
            for token in ne:
                term += " "+token[0]
            terms.append(term)

        terms.sort(key=lambda x: self.text.find(x))

        self.ners = terms
        return self.ners

    def _ner_traverse(self,t):
        ne = [
            'ORGANIZATION',
            'PERSON',
            'LOCATION',
            'FACILITY',
            'GPE'
        ]
        try:
            t.node
        except AttributeError:
            return
        else:
            if t.node in ne:
                try:
                    self._ne_count[str(t)] += 1
                except:
                    pass
                if t not in self._ne:
                    self._ne.append(t)
            else:
                for child in t:
                    self._ner_traverse(child)

    def parse(self):
        if not self.ners:
            self.ner()
        return self.ners