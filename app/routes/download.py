# app/routes/download.py
from flask import Blueprint, render_template

download_bp = Blueprint('download', __name__)

@download_bp.route('/download')
def index():
    return render_template('download.html')
