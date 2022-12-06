#!/usr/bin/python3
"""Routes on the api itself, like status"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def show_status():
    status = {
        "status": "OK"
    }

    return jsonify(status)
