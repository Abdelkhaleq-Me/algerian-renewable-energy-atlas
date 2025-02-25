# app/errors.py
from flask import render_template, jsonify, request
from app.extensions import db  # Import if you need database access in error handlers

def handle_404_error(e):
    # Log the error (optional but recommended)
    db.get_app().logger.error(f'404 Not Found: {e}') # Use the app logger

    # Check if the request accepts JSON (likely an API request)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found.'}), 404

    # Otherwise, render an HTML error page
    return render_template('errors/404.html'), 404


def handle_500_error(e):
     # Log the error (important for debugging)
    db.get_app().logger.error(f'500 Internal Server Error: {e}')

    # Rollback any database changes (important to prevent data corruption)
    db.session.rollback()

    # Check if it's an API request
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred.'}), 500

    return render_template('errors/500.html'), 500

def handle_400_error(e):
     # Log the error
    db.get_app().logger.error(f'400 Bad Request Error: {e}')

    # Check if it's an API request
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
      return jsonify({'error': 'Bad Request', 'message': str(e)}), 400 # Use str(e) to get a description

    return render_template('errors/400.html'), 400

def handle_403_error(e):
     # Log the error
    db.get_app().logger.error(f'403 Bad Request Error: {e}')

    # Check if it's an API request
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
       return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to access this resource.'}), 403

    return render_template('errors/403.html'), 403

def init_app(app):
    app.errorhandler(400)(handle_400_error)
    app.errorhandler(403)(handle_403_error)
    app.errorhandler(404)(handle_404_error)
    app.errorhandler(500)(handle_500_error)