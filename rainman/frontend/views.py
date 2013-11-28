"""
Views for the Rainman frontend.
"""
from flask import Blueprint, render_template

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def home():
    """
    Render static homepage
    """
    return render_template('index.html')