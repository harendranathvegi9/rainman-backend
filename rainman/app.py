import os
from flask import Flask, request, jsonify, render_template

from decorators import crossdomain

from api import api



app = Flask(__name__)

app.register_blueprint(api)

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

@app.route('/')
def home():
  return render_template('index.html')

