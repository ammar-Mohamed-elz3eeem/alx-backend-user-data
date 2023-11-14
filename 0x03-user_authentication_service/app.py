#!/usr/bin/env python3
"""hash password module"""
from user import User
from db import DB
from flask import jsonify, Flask, request, abort, make_response, redirect
from auth import Auth


AUTH = Auth()
app = Flask("__main__")


@app.route("/", methods=["GET"], strict_slashes=False)
def home_page():
    """Homepage route"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Users post route to register new users"""
    try:
        email = request.form['email']
        password = request.form['password']
    except Exception:
        return abort(400)

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Users post reoute to login them in system"""
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    if not AUTH.valid_login(email, password):
        return abort(401)

    sess_id = AUTH.create_session(email)
    res = make_response(jsonify({"email": f"{email}",
                                 "message": "logged in"}), 200)
    res.set_cookie("session_id", sess_id)
    return res


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """destroy user's session"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        return abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        return abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    """get current logged in user profile"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        return abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        return abort(403)
    return jsonify({"email": f"{user.email}"}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """get reset password token for the user"""
    email = request.form.get("email", "")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"})
    except Exception:
        return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
