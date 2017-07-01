
from flask import request
from backplate_auth import AuthTokenFlowBase
from auth.sessions import AuthTokenSessions

class AuthFlow(AuthTokenSessions, AuthTokenFlowBase):
    def resolve_request_user_id(self):
        user_id = 47
        if request.args.get('chicken') == '':
            return user_id
        return None

    def resolve_user_id(self, user_id):
        if user_id == 47:
            return {
                'id': user_id,
                'name': 'Agent 47'
            }
        return None

flow = AuthFlow()

__all__ = ['AuthFlow', 'flow']
