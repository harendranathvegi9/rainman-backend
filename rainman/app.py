import os
from flask import Flask, request, jsonify, render_template

from api import api
from frontend import frontend

app = Flask(__name__)
from config import config, logs

app.register_blueprint(api)
app.register_blueprint(frontend)