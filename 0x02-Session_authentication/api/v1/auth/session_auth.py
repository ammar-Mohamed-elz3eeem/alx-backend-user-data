#!/usr/bin/env python3
""" Module of SessionAuth Class
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """template for all session authentication system
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create session for user_id and save it in the dictionary"""
        if type(user_id) is not str or user_id is None:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retrieve user id using his session id"""
        if type(session_id) is not str or session_id is None:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """retrieve user using it's session id"""
        sess_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sess_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """destroy session from the session store"""
        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if sess_id is None:
            return False
        if self.user_id_for_session_id(sess_id) is None:
            return False
        del SessionAuth.user_id_by_session_id[sess_id]
        return True
