#!/usr/bin/python3
"""Handles all RESTful API actions for Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities')
def get_amenities():
    """GET all amenities"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>')
def get_amenity(amenity_id):
    """GET a single amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"])
def delete_amenity(amenity_id):
    """DELETE a single amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return {}, 200


@app_views.route('/amenities', methods=["POST"])
def create_amenity():
    """POST/CREATE a single amenity"""
    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        elif req.get('name') is None:
            abort(400, description="Missing name")
        else:
            created = Amenity(**req)
            storage.new(created)
            storage.save()
            return jsonify(created.to_dict()), 201
    except ValueError:
        abort(400, description="Not a JSON")


@app_views.route('/amenities/<amenity_id>', methods=["PUT"])
def update_amenity(amenity_id):
    """PUT/UPDATE a single amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'created_at', 'updated_at']
            for key, value in req.items():
                if key not in invalid:
                    setattr(amenity, key, value)
            storage.save()
            return jsonify(amenity.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
