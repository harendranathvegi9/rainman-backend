from flask import Blueprint, request, jsonify
from ..helpers.decorators import crossdomain
from ..parser import Parser

api = Blueprint('api', __name__, url_prefix='/api')

@crossdomain(origin='*', headers=["Accept", "Content-Type"])
@api.route('/article', methods=['POST', 'OPTIONS'])
def article():
    r = request.get_json()
    content = r['content']
    domain = r['url']
    p = Parser(content, domain)
    return p.parse()