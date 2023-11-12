#!/usr/bin/env python3
""" Module of SessionDBAuth  Class
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import timedelta, datetime
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """template for all session authentication system
    that is limited by expiration date and saved on db"""

    def create_session(self, user_id=None):
        """create session for user_id and save it in the dictionary"""
        session_id = super().create_session(user_id)
        
        if session_id is None:
            return None

        user_sess = UserSession(**{"user_id": user_id, "session_id": session_id})
        user_sess.save()
        UserSession.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """using session id to validate session info"""
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_sess = UserSession.search({"session_id": session_id})

        if user_sess is None or len(user_sess) == 0:
            return None
        user_sess = user_sess[0]
        if self.session_duration <= 0:
            return user_sess.user_id
        expired = user_sess.created_at + \
            timedelta(seconds=self.session_duration)
        if expired < datetime.utcnow():
            return None

        return user_sess.user_id

    def destroy_session(self, request=None):
        """using request object to get session data from cookie"""
        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if sess_id is None:
            return False
        user_id = self.user_id_for_session_id(sess_id)
        if not user_id:
            return False
        user_sess = UserSession.search({"session_id": sess_id})
        if user_sess is None or len(user_sess) == 0:
            return False
        try:
            user_sess[0].remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
