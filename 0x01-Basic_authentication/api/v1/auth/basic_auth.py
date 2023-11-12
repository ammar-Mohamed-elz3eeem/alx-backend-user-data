#!/usr/bin/env python3
"""
Basic Authentication of api endpoints
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


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

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """check that userinfo is same info found in database"""
        if not isinstance(user_email, str):
            return None
        if not isinstance(user_pwd, str):
            return None
        User.load_from_file()
        print(User.all())
        user = User.search({"email": user_email})
        print(user)
        if len(user) == 0:
            return None
        if not user[0].is_valid_password(user_pwd):
            print("password is invalid")
            return None
        print("password is valid")
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """get current user from the autherization key"""
        user_tuple = self.extract_user_credentials(
                self.decode_base64_authorization_header(
                    self.extract_base64_authorization_header(
                        self.authorization_header(request))))
        return self.user_object_from_credentials(user_tuple[0], user_tuple[1])
