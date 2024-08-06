#!/usr/bin/python3
'''This module contains the routes and methods for handling the amenities
endpoint of the API. It supports various HTTP methods to interact with
amenity resources.
'''

from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

# List of allowed HTTP methods for the amenities endpoint
ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
'''Methods allowed for the amenities endpoint.'''

@app_views.route('/amenities', methods=ALLOWED_METHODS)
@app_views.route('/amenities/<amenity_id>', methods=ALLOWED_METHODS)
def handle_amenities(amenity_id=None):
    '''Handles requests to the /amenities and /amenities/<amenity_id> endpoints.
    
    The behavior of this function depends on the HTTP method of the request:
    - GET: Retrieves a list of all amenities or a specific amenity by id.
    - DELETE: Deletes a specific amenity by id.
    - POST: Creates a new amenity.
    - PUT: Updates an existing amenity by id.

    Args:
        amenity_id (str, optional): The id of the amenity to operate on. Default is None.

    Returns:
        Response: JSON response with the status and data according to the operation performed.

    Raises:
        MethodNotAllowed: If the HTTP method is not allowed.
    '''
    handlers = {
        'GET': get_amenities,
        'DELETE': remove_amenity,
        'POST': add_amenity,
        'PUT': update_amenity,
    }
    if request.method in handlers:
        return handlers[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_amenities(amenity_id=None):
    '''Retrieves amenities. Can return either a list of all amenities or
    a specific amenity by id.

    Args:
        amenity_id (str, optional): The id of the amenity to retrieve. Default is None.

    Returns:
        Response: JSON response with the amenity data or a list of all amenities.

    Raises:
        NotFound: If the amenity with the specified id is not found.
    '''
    all_amenities = storage.all(Amenity).values()
    if amenity_id:
        res = list(filter(lambda x: x.id == amenity_id, all_amenities))
        if res:
            return jsonify(res[0].to_dict())
        raise NotFound()
    all_amenities = list(map(lambda x: x.to_dict(), all_amenities))
    return jsonify(all_amenities)


def remove_amenity(amenity_id=None):
    '''Deletes an amenity by id.

    Args:
        amenity_id (str): The id of the amenity to delete.

    Returns:
        Response: JSON response with a 200 status code indicating successful deletion.

    Raises:
        NotFound: If the amenity with the specified id is not found.
    '''
    all_amenities = storage.all(Amenity).values()
    res = list(filter(lambda x: x.id == amenity_id, all_amenities))
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_amenity(amenity_id=None):
    '''Creates a new amenity.

    Args:
        amenity_id (str, optional): This parameter is not used when adding a new amenity. Default is None.

    Returns:
        Response: JSON response with the created amenity data and a 201 status code.

    Raises:
        BadRequest: If the request body is not JSON or missing required fields.
    '''
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


def update_amenity(amenity_id=None):
    '''Updates an existing amenity by id.

    Args:
        amenity_id (str): The id of the amenity to update.

    Returns:
        Response: JSON response with the updated amenity data and a 200 status code.

    Raises:
        NotFound: If the amenity with the specified id is not found.
        BadRequest: If the request body is not JSON.
    '''
    xkeys = ('id', 'created_at', 'updated_at')
    all_amenities = storage.all(Amenity).values()
    res = list(filter(lambda x: x.id == amenity_id, all_amenities))
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_amenity = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_amenity, key, value)
        old_amenity.save()
        return jsonify(old_amenity.to_dict()), 200
    raise NotFound()

