#!/usr/bin/env python3
""" Module of Auth Class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """template for all authentication system
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check if path required authentication or not"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if "{}/".format(path) in excluded_paths or path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """check that header have authorization string"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """get current user from the autherization key"""
        return None
