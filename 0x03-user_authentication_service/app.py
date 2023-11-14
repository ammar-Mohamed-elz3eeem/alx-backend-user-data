#!/usr/bin/env python3
"""hash password module"""
from user import User
from db import DB
from flask import jsonify, Flask, request, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
