import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
	return 'Hello World!'
@app.route('/api', methods=['POST'])
def parse():
	#assert request.path is '/api'
	#assert request.method is 'POST'
	return request


if __name__ == '__main__':
	app.run()