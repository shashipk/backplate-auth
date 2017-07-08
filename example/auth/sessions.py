
from uuid import uuid4
from backplate_auth import AuthTokenSessionsBase

sessions = {}

def create_session(user_id):
    session = str(uuid4()).split('-')[0]
    if user_id not in sessions:
        sessions[user_id] = [session]
    else:
        sessions[user_id].append(session)
    return session

def remove_session(session):
    if session:
        for user_id in sessions:
            if session in sessions.get(user_id, []):
                sessions[user_id].remove(session)

class AuthTokenSessions(AuthTokenSessionsBase):
    def check_session(self, session, user_id):
        if session in sessions.get(user_id, []):
            return True
        return False

    def get_session(self, user_id):
        return create_session(user_id)
