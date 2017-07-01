
from webargs.flaskparser import use_args
from backplate_auth import create_auth_endpoint

from auth import flow
from auth.sessions import remove_session

AuthBase = create_auth_endpoint(flow)

class Auth(AuthBase):
    @use_args(flow.endpoint_args)
    def delete(self, args):
        token = args.get('token')
        if token:
            flow.check_token(token)
            session = flow.get_token_session(token)
            remove_session(session)

        return None, 204

__all__ = ['Auth']
