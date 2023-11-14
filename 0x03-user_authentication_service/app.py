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
    try:
        email = request.form['email']
        password = request.form['password']
    except Exception:
        return abort(400)

    if AUTH.valid_login(email, password):
        sess_id = AUTH.create_session(email)
        res = Response(jsonify({"email": f"{email}",
                                "message": "logged in"
                                }),
                       200).set_cookie("session_id", sess_id)
        return res
    else:
        return abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
