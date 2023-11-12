#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_user_route():
    """log user in using form data"""
    user_email = request.form.get("email")
    user_pwd = request.form.get("password")
    if not user_email or user_email is None:
        return jsonify({"error": "email missing"}), 400
    if not user_pwd or user_pwd is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": user_email})
    if user is None or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(user_pwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    from os import getenv

    sess_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), sess_id)
    return response, 200


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def delete_session_route():
    """route for making logout request to server"""
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if is_destroyed:
        return jsonify({}), 200
    abort(404)
