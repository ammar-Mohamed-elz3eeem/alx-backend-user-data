#!/usr/bin/env python3
"""hash password module"""
import bcrypt
import uuid
from db import DB
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Authentication constructor"""
        self._db = DB()

    def register_user(self, email: str, password: str):
        """Register new user with email and password"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hpassword = _hash_password(password)
            return self._db.add_user(email, hpassword)
        else:
            raise ValueError("User {} already exists".format(email))

    def valid_login(self, email, password):
        """check login credentials for user when logging"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(str(password).encode(), user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str):
        """generate session for user when he logs in"""
        sess_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=sess_id)
            return sess_id
        except Exception:
            return None


def _hash_password(passwd: str):
    """hash given password string using bcrypt"""
    return bcrypt.hashpw(passwd.encode(), bcrypt.gensalt(10))


def _generate_uuid():
    return str(uuid.uuid4())
