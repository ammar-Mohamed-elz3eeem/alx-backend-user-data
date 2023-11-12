#!/usr/bin/env python3
""" Module of SessionAuth Class
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """template for all session authentication system
    """

    user_id_by_session_id = {}


    def create_session(self, user_id: str = None) -> str:
        if type(user_id) is not str or user_id is None:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        if type(session_id) is not str or session_id is None:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)
