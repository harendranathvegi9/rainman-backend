import os
from flask import Flask, request,jsonify
import nltk
from readability.readability import Document

MIN_LEN = 200

app = Flask(__name__)

class RainError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(RainError)
def handle_error(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

class Filters:

	def named_entites(content, domain):
		
		return content, []

	def wikipedia(content,domain):
		cards = ['Hello']
		return content,cards

	functions = [named_entites, wikipedia]

def rainman(full_html, domain):
	content = parse(full_html, domain)
	content, cards = run_filters(content, domain)

	return content['readable']

	return jsonify(content=content['readable'], cards=cards)

def parse(full_html, domain):
	readable_html = readable(full_html, domain)
	raw = nltk.clean_html(readable_html)
	content = {}
	content['raw'] = raw
	content['readable'] = readable_html
	checkArticle(content, domain)
	return content

def run_filters(content, domain):
	cards = []
	filters = Filters()

	for f in filters.functions:
		fcontent, fcards = f(content, domain)
		content = fcontent
		cards.extend(fcards)

	return content, cards

def readable(full_html, domain):
	positive, negative = article_patterns(domain)
	readable_html = Document(full_html, positive_keywords=positive, negative_keywords=negative).summary()
	return readable_html

def article_patterns(domain):
	return [],[]

def checkArticle(content, domain):
	whitelist = []
	blacklist = []
	if (content['raw'].__len__() < MIN_LEN or domain in blacklist) and (domain not in whitelist):
		raise RainError('Not an article')

@app.route('/')
def home():
	return 'Hello World!'

@app.route('/api', methods=['POST'])
def api():
	content = request.form['content']
	domain = request.form['domain']
	return rainman(content, domain)

if __name__ == '__main__':
	app.run(debug=True)