#!/usr/bin/env python3
""" Module of Auth Class
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """template for all authentication system
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check if path required authentication or not"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for ex_path in excluded_paths:
            if "*" in ex_path:
                if path.startswith(ex_path[:-1]):
                    return False
            if "{}/".format(path) == ex_path or path == ex_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """check that header have authorization string"""
        if request is None:
            return None
        if request.headers.get("Authorization") is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """get current user from the autherization key"""
        return None

    def session_cookie(self, request=None):
        """get the session from the request"""
        if request is None:
            return None
        SESSION_NAME = getenv("SESSION_NAME", None)
        if SESSION_NAME is None:
            return None
        return request.cookies.get(SESSION_NAME)
