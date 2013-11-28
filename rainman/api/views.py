"""
A Flask blueprint for the Rainman API
"""
from flask import Blueprint, request, jsonify
from ..helpers.decorators import crossdomain
from ..parser import Parser

api = Blueprint('api', __name__, url_prefix='/api')

# API must accept all content types for correct CORS behavior
@crossdomain(origin='*', headers=["Accept", "Content-Type"])
# API must accept OPTIONS method for CORS pre-flight requests
@api.route('/article', methods=['POST', 'OPTIONS'])
def article():
    """
    Returns the context items for a given article, as well
    as the readability version of the article.

    The JSON response has the following properties:
    - `cards` : an array of card objects with the following properties
        - `images` : a list of image URLs for the card term
        - `summary` : a summary of the Wikipedia article
        - `title` : the term title
        - `url` : the URL to the full Wikipedia article
    - `content` : the readability formatted article body
    - `title` : the title of the article itself
    """
    r = request.get_json()
    content = r['content']
    domain = r['url']
    p = Parser(content, domain)
    return p.parse()