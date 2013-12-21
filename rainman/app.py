"""
Runs the app, sets up config & logging, and registers blueprints
"""
import os
from flask import Flask, request, jsonify, render_template

from api import api

app = Flask(__name__)

# Config & logs must be imported after the app is created
# because they modify the current_app Flask object
from config import config, logs

# All views are registered as blueprints
app.register_blueprint(api)