# app/routes/download.py
from flask import Blueprint, render_template

download_bp = Blueprint('download', __name__, url_prefix='/download')

@download_bp.route('/')
def index():
    return render_template('download.html')
