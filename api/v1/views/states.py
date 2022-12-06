#!/usr/bin/python3
"""Handles all RESTful API actions for State objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states')
def get_states():
    """GET all states"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>')
def get_state(state_id):
    """GET a single state"""
    found = storage.get(State, state_id)
    if not found:
        abort(404)


@app_views.route('/states/<state_id>', methods=["DELETE"])
def delete_state(state_id):
    """DELETE a single state"""
    found = storage.get(State, state_id)
    if not found:
        return {}, 200
    else:
        storage.delete(found)
        storage.save()


@app_views.route('/states', methods=["POST"])
def create_state():
    """POST/CREATE a single state"""
    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
    except ValueError:
        abort(400, description="Not a JSON")
