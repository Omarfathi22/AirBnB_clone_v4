#!/usr/bin/python3
'''This script contains a Flask web application API that serves as the entry point
for the REST API. It initializes the Flask application, sets up routing, error handling,
and integrates CORS for cross-origin requests.
'''

import os
from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views

# Create a Flask web application instance
app = Flask(__name__)
'''The Flask web application instance.'''

# Retrieve host and port configurations from environment variables
# Defaults are set to '0.0.0.0' for the host and '5000' for the port.
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))

# Configure the Flask application to not enforce strict slashes in URL paths
app.url_map.strict_slashes = False

# Register the blueprints from the 'api.v1.views' module to handle API routes
app.register_blueprint(app_views)

# Enable Cross-Origin Resource Sharing (CORS) for the Flask application
# This allows requests from any origin (specified by '/*') to be accepted.
CORS(app, resources={'/*': {'origins': app_host}})

@app.teardown_appcontext
def teardown_flask(exception):
    '''Callback function that is called when the Flask application context ends.
    It ensures that resources are properly cleaned up, including closing the 
    storage connection.
    '''
    # Uncomment the line below to print exception details (if any) during teardown
    # print(exception)
    storage.close()

@app.errorhandler(404)
def error_404(error):
    '''Handler for 404 HTTP error code (Not Found).
    Returns a JSON response with an error message and a 404 status code.
    '''
    return jsonify(error='Not found'), 404

@app.errorhandler(400)
def error_400(error):
    '''Handler for 400 HTTP error code (Bad Request).
    Returns a JSON response with an error message and a 400 status code.
    If the error has a description attribute, it uses that as the error message.
    '''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400

if __name__ == '__main__':
    # Retrieve host and port configurations again for running the app
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    
    # Run the Flask application with specified host, port, and threaded mode enabled
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )

