#!/usr/bin/python3
"""Handles all RESTful API actions for Review objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews')
def get_reviews(place_id):
    """GET all Review objects of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>')
def get_review(review_id):
    """GET a single review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=["DELETE"])
def delete_review(review_id):
    """DELETE a single review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return {}, 200


@app_views.route('/places/<place_id>/reviews', methods=["POST"])
def create_review(place_id):
    """POST/CREATE a single review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        elif req.get('user_id') is None:
            abort(400, description="Missing user_id")
        elif storage.get(User, req.get('user_id')) is None:
            abort(404)
        elif req.get('text') is None:
            abort(400, description="Missing text")
        else:
            created = Review(**req)
            created.place_id = place.id
            storage.new(created)
            storage.save()
            return jsonify(created.to_dict()), 201
    except ValueError:
        abort(400, description="Not a JSON")


@app_views.route('/reviews/<review_id>', methods=["PUT"])
def update_review(review_id):
    """PUT/UPDATE a single review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    try:
        req = request.get_json()
        if req is None:
            abort(400, description="Not a JSON")
        else:
            invalid = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
            for key, value in req.items():
                if key not in invalid:
                    setattr(review, key, value)
            storage.save()
            return jsonify(review.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
