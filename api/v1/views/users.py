#!/usr/bin/python3
"""Handles all RESTful API actions for User objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users')
def get_users():
    """GET all users"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>')
def get_user(user_id):
    """GET a single user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    """DELETE a single user"""
    user = storage.get(User, user_id)
    if not user:
        return {}, 404
    else:
        storage.delete(user)
        storage.save()
        return {}, 200


@app_views.route('/users', methods=["POST"])
def create_user():
    """POST/CREATE a single user"""
    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        elif req.get('email') is None:
            abort(400, description="Missing email")
        elif req.get('password') is None:
            abort(400, description="Missing password")
        else:
            created = User(**req)
            storage.new(created)
            storage.save()
            return jsonify(created.to_dict()), 201
    except ValueError:
        abort(400, description="Not a JSON")


@app_views.route('/users/<user_id>', methods=["PUT"])
def update_user(user_id):
    """PUT/UPDATE a single user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'created_at', 'updated_at']
            for key, value in req.items():
                if key not in invalid:
                    setattr(user, key, value)
            storage.save()
            return jsonify(user.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
