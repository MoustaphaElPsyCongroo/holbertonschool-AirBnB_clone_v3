#!/usr/bin/python3
"""Handles all RESTful API actions for City objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities')
def get_cities(state_id):
    """GET all City objects of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]

    return jsonify(cities)


@app_views.route('/cities/<city_id>')
def get_city(city_id):
    """GET a single city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=["DELETE"])
def delete_city(city_id):
    """DELETE a single city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return {}, 200


@app_views.route('/states/<state_id>/cities', methods=["POST"])
def create_city(state_id):
    """POST/CREATE a single city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        elif req.get('name') is None:
            abort(400, description="Missing name")
        else:
            created = City(**req)
            created.state_id = state.id
            storage.new(created)
            storage.save()
            return jsonify(created.to_dict()), 201
    except ValueError:
        abort(400, description="Not a JSON")


@app_views.route('/cities/<city_id>', methods=["PUT"])
def update_city(city_id):
    """PUT/UPDATE a single city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'created_at', 'updated_at']
            for key, value in req.items():
                if key not in invalid:
                    setattr(city, key, value)
            storage.save()
            return jsonify(city.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
