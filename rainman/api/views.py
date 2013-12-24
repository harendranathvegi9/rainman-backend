"""
A Flask blueprint for the Rainman API
"""
from flask import Blueprint, request, jsonify
from ..helpers.decorators import crossdomain
from ..lib.parser import Document

import urllib

api = Blueprint('api', __name__)

@api.route('/', methods=['POST'])
# API must accept all content types for correct CORS behavior
@crossdomain(origin='*', headers=["Accept", "Content-Type"])
def parse():
    """
    Returns the context items for a given article.
    """
    r = request.get_json()
    d = Document(r['title'], r['text'], r['domain'])
    entities = d.entities()
    return jsonify(entities=entities)

@api.route('/admin', methods=['POST'])
# API must accept all content types for correct CORS behavior
@crossdomain(origin='*', headers=["Accept", "Content-Type"])
def admin():
    """
    Returns the context items for a given article, along with
    verbose information about each entity.
    """
    r = request.get_json()
    d = Document(r['title'], r['text'], r['domain'])
    entities = d.entities(verbose=True)
    return jsonify(entities=entities)