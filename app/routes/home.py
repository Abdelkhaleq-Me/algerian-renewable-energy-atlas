# app/routes/home.py
from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    # Render your home page template or return a simple response for now.
    return render_template('home.html')
