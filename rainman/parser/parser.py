from flask import jsonify
from readability.readability import Document
import wikipedia

from collections import defaultdict
import json
import simplejson

import nltk

nltk.data.path.append('./nltk_data/')

MIN_LEN = 0

class Filters:

    def __init__(self):
        self._ne = []
        self._ne_count = defaultdict(int)
        self.functions = [self.named_entities]
        return

    def named_entities(self, content, domain):
        sentences = nltk.sent_tokenize(content['raw'].encode('utf-8'))
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        trees = nltk.batch_ne_chunk(sentences)
        for tree in trees:
            self._traverse(tree)
        self._ne.sort(key=lambda x: self._ne_count[str(x)], reverse=True)

        terms = []
        for ne in self._ne:
            term = ""
            for token in ne:
                term += " "+token[0]
            terms.append(term)

        terms = terms[:10]

        terms.sort(key=lambda x: content['raw'].find(x))

        cards = []
        for term in terms:
            try:
                card = self._wikipedia_card(term)
                if card['title'] not in [c['title'] for c in cards]:
                    cards.append(card)
                print card.title
            except:
                pass        

        return content, cards

    def _traverse(self,t):
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
                    self._traverse(child)

    def tokenize_words(self, content, domain):
        content['tokens'] = nltk.word_tokenize(content['raw'].encode('utf-8'))
        return content, []

    def _wikipedia_card(self,query):
        try:
            page = wikipedia.page(query)
        except:
            return False
        card = {}
        card['title'] = page.title
        card['url'] = page.url
        card['summary'] = page.summary
        card['images'] = [image for image in page.images if self._filter_image(image)]
        card['images'] = card['images'][:4]
        return card

    def _filter_image(self,image):
        return ("commons" in image) and image.endswith('.jpg')

    def collocations(self,content, domain):
        text = nltk.Text(content['tokens'])
        collocations = self._collocations_from_text(text)
        cards = []
        #collocations = ['White House','health care', 'West Wing', 'Mr. Obama', 'said, ','Mr. Obama\'s', 'said one', 'Wing staff', 'Democratic lawmakers', 'staff members','President Obama', 'White House.', 'care problems', 'Mr. McDonough', 'senior']
        for phrase in collocations:
            card = self._wikipedia_card(phrase)

            cards.append(card)
        return content, cards

    def _collocations_from_text(self,text):
        window_size = 2
        num = 20
        from nltk.corpus import stopwords
        from nltk.metrics import f_measure, BigramAssocMeasures, TrigramAssocMeasures
        from nltk.collocations import BigramCollocationFinder, TrigramCollectionFinder
        ignored_words = stopwords.words('english')
        finder = BigramCollocationFinder.from_words(text.tokens, window_size)
        finder.apply_freq_filter(2)
        finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
        bigram_measures = BigramAssocMeasures()
        trigram_measures = TrigramAssocMeasures()
        collocations = finder.nbest(bigram_measures.likelihood_ratio,num)
        colloc_strings = [w1+' '+w2 for w1, w2 in collocations]
        return colloc_strings

    def _similar_terms(self, term1, term2):
        import difflib
        return difflib.SequenceMatcher(a=term1.lower(), b=term2.lower()).ratio() > 0.5

class Parser:
    def __init__(self, content, domain):
        self.content = content
        self.domain = domain

    def parse(self):
        content = self.text(self.content, self.domain)
        cards = []
        content, cards = self.run_filters(content, self.domain)

        data = jsonify(content=content['readable'], cards=cards, title=content['title'])
        return data

    def text(self, full_html, domain):
        readable_html, title = self.readable(full_html, domain)
        raw = nltk.clean_html(readable_html)
        content = {}
        content['raw'] = raw
        content['readable'] = readable_html
        content['title'] = title
        self.checkArticle(content, domain)
        return content

    def run_filters(self, content, domain):
        cards = []
        filters = Filters()
        for f in filters.functions:
            fcontent, fcards = f(content, domain)
            content = fcontent
            cards.extend(fcards)
        return content, cards

    def readable(self, full_html, domain):
        positive, negative = [],[]
        doc = Document(full_html, positive_keywords=positive, negative_keywords=negative)
        readable_html = doc.summary()
        title = doc.short_title()
        print title
        return readable_html, title

    def checkArticle(self, content, domain):
        whitelist = []
        blacklist = []
        if (content['raw'].__len__() < MIN_LEN or domain in blacklist) and (domain not in whitelist):
            raise Error('Not an article')