#!/usr/bin/env python3
""" UserSession module
"""
import hashlib
from models.base import Base
import uuid


class UserSession(Base):
    """ UserSession class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """initialize new UserSession Object"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
