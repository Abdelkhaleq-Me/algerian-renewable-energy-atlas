# app/routes/atlas.py
from flask import Blueprint, render_template

atlas_bp = Blueprint('atlas', __name__, url_prefix='/atlas')

@atlas_bp.route('/')
def index():
    return render_template('atlas.html')
