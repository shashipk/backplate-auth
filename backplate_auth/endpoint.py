
from webargs.flaskparser import use_args
from flask_restful import Resource

from .error import AuthTokenError

def create_auth_endpoint(AuthFlow):

    flow = AuthFlow

    class AuthEndpoint(Resource):

        @use_args(flow.endpoint_args)
        def post(self, args):
            user_id = None
            token = args.get('token')
            if token:
                flow.check_token(token)
                user_id = flow.resolve_token_user_id(token)
            else:
                user_id = flow.resolve_request_user_id()
                if not user_id:
                    raise AuthTokenError("Could not resolve user from request.")

            payload = flow.create_token_payload(user_id)
            token = flow.jwt.create(payload)

            return {'token': token}

    return AuthEndpoint
