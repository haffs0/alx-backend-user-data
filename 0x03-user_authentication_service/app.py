#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request, abort, redirect


from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def status():
    """testing"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """POST /users
    return:
        user playload
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /users
    return:
        user data
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    return:
        redirct GET /
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    return:
        user playload
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")