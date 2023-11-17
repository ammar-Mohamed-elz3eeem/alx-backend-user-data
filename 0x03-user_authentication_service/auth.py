#!/usr/bin/env python3
"""hash password module"""
import bcrypt
import uuid
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Authentication constructor"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register new user with email and password"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hpassword = _hash_password(password)
            return self._db.add_user(email, hpassword)
        else:
            raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """check login credentials for user when logging"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(str(password).encode(), user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """generate session for user when he logs in"""
        sess_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=sess_id)
            return sess_id
        except Exception:
            return None

    def get_user_from_session_id(self, sess_id: str) -> User:
        """get user info from his associated session id"""
        if not sess_id:
            return None
        try:
            return self._db.find_user_by(session_id=sess_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy user session in db using update method"""
        if not user_id:
            return None
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """generate reset password token for user to make them
        able to change thier passwords"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> str:
        """update user passwords after checking thier reset token
        assigned to them"""
        if reset_token is None or password is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)


def _hash_password(password: str) -> str:
    """hash given password string using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """generates random uuid"""
    return str(uuid.uuid4())
