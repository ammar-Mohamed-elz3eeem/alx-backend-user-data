#!/usr/bin/env python3
"""
Basic Authentication of api endpoints
"""
from api.v1.auth.auth import Auth
from base64 import b64decode


class BasicAuth(Auth):
    """this class will be used for basic authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """get the base64 version of authorization key"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """decode authorization header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = b64decode(base64_authorization_header).decode()
            return decoded
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """extract returns the user email and
        password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(":")
        return (credentials[0], credentials[1])
