#!/usr/bin/python3
"""Handles all RESTful API actions for Place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places')
def get_places(city_id):
    """GET all Place objects of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route('/places/<place_id>')
def get_place(place_id):
    """GET a single place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=["DELETE"])
def delete_place(place_id):
    """DELETE a single place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return {}, 200


@app_views.route('/cities/<city_id>/places', methods=["POST"])
def create_place(city_id):
    """POST/CREATE a single place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        elif req.get('user_id') is None:
            abort(400, description="Missing user_id")
        elif storage.get(User, req.get('user_id')) is None:
            abort(404)
        elif req.get('name') is None:
            abort(400, description="Missing name")
        else:
            created = Place(**req)
            created.city_id = city.id
            storage.new(created)
            storage.save()
            return jsonify(created.to_dict()), 201
    except ValueError:
        abort(400, description="Not a JSON")


@app_views.route('/places/<place_id>', methods=["PUT"])
def update_place(place_id):
    """PUT/UPDATE a single place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for key, value in req.items():
                if key not in invalid:
                    setattr(place, key, value)
            storage.save()
            return jsonify(place.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
