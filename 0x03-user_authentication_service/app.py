#!/usr/bin/env python3
"""hash password module"""
from user import User
from db import DB
from flask import jsonify, Flask, request, abort, Response
from auth import Auth


AUTH = Auth()
app = Flask("__main__")


@app.route("/", methods=["GET"], strict_slashes=True)
def home_page():
    """Homepage route"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=True)
def users():
    """Users post route to register new users"""
    try:
        email = request.form['email']
        password = request.form['password']
    except Exception:
        abort(400)

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=True)
def login():
    """Users post reoute to login them in system"""
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    if not AUTH.valid_login(email, password):
        return abort(401)

    sess_id = AUTH.create_session(email)
    res = Response(jsonify({"email": f"{email}", "message": "logged in"}), 200)
    res.set_cookie("session_id", sess_id)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
