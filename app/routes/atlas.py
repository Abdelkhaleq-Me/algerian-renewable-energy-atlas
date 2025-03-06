# app/routes/atlas.py
from flask import Blueprint, render_template

atlas_bp = Blueprint('atlas', __name__)

@atlas_bp.route('/atlas')
def index():
    return render_template('atlas.html')
