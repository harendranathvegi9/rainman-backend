"""
A Flask blueprint for the Rainman API
"""
from flask import Blueprint, request, jsonify
from ..helpers.decorators import crossdomain
from ..parser import Parser

api = Blueprint('api', __name__)

@api.route('/', methods=['POST'])
# API must accept all content types for correct CORS behavior
@crossdomain(origin='*', headers=["Accept", "Content-Type"])
def parse():
    """
    Returns the context items for a given article.
    """
    r = request.get_json()
    p = Parser(r['title'], r['text'], r['domain'])
    ne = p.parse()
    return jsonify(ne=ne)

@api.route('/admin', methods=['POST'])
# API must accept all content types for correct CORS behavior
@crossdomain(origin='*', headers=["Accept", "Content-Type"])
def admin():
    """
    Returns the context items for a given article, along with
    results from each step of the NLP algorithm.
    """
    r = request.get_json()
    p = Parser(r['title'], r['text'], r['domain'])
    tagged = p.tag()
    ne = p.ner()
    return jsonify(ne=ne)