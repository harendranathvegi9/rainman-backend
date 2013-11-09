import os
from flask import Flask, request,jsonify

app = Flask(__name__)

def rainman(content, domain):
	cards = []
	return jsonify(content=content, cards=cards)

@app.route('/')
def home():
	return 'Hello World!'

@app.route('/api', methods=['POST'])
def api():
	content = request.args['content']
	domain = request.args['domain']
	return rainman(content, domain)

if __name__ == '__main__':
	app.run(debug=True)