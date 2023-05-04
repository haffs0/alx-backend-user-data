#!/usr/bin/env python3
"""Module of Users views.
"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, request
from typing import Tuple
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login
    Return:
      - list of User objects JSON represented.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    if users[0].is_valid_password('password'):
        from api.v1.app import auth

        session_id = auth.create_session(users[0].user_id)
        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return res
    return jsonify({"error": "wrong password"}), 401
