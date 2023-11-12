#!/usr/bin/env python3
""" Module of SessionAuth Class
"""
# from flask import request
# from typing import List, TypeVar
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta
# from models.user import User
# import uuid


class SessionExpAuth(SessionAuth):
    """template for all session authentication system
    that is limited by expiration date"""

    def __init__(self) -> None:
        """init session duration to be equal to
        SESSION_DURATION environment variable"""

        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create session using user id with
        created_at added to it to limit it by expiration time"""

        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        SessionExpAuth.user_id_by_session_id[sess_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """using session id to validate session info
        and session duration"""

        if session_id is None:
            return None
        sess_info = SessionExpAuth.user_id_by_session_id.get(session_id)
        if sess_info is None:
            return None
        if self.session_duration <= 0:
            return sess_info.get("user_id")
        created_at = sess_info.get("created_at")
        if created_at is None:
            return None
        expiration_date = created_at + timedelta(seconds=self.session_duration)
        if expiration_date < datetime.now():
            return None
        return sess_info.get("user_id")
