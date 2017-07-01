
from flask import request
from webargs import fields

from .jwt import JWT
from .error import AuthTokenError

class AuthFlowBase:
    jwt_args = {}
    endpoint_args = {'token': fields.String()}

    def __init__(self):
        self.jwt = JWT(**self.jwt_args)

    # Required overrides

    def resolve_request_user_id(self):
        """
        Required override!
        Return a user id from the request object.
        Returning None will cause an validation error.
        """
        raise NotImplementedError

    def check_user_id(self, user_id):
        """
        Required override!
        Return a boolean after checking user_id with database.
        Returning False will cause an validation error.
        """
        raise NotImplementedError

    def resolve_user_id(self, user_id):
        """
        Required override!
        Return an object that represents the user from database user_id.
        Returning None may result in errors.
        """
        raise NotImplementedError

    # Optional overrides

    def create_token_payload(self, user_id):
        """
        Optional override.
        Return a dictionary containing at least the 'uid' of user.
        """
        return {'uid': user_id}

    def check_token_payload(self, payload):
        """
        Optional override.
        Return a boolean after running additional validation checks.
        Returning False will cause an validation error.
        """
        return True

    def resolve_token_payload(self, token):
        """
        Optional override.
        Return a dictionary from the given token payload.
        Return None will cause a validation error.
        """
        payload = self.jwt.parse(token)
        return payload

    def resolve_token_user_id(self, token):
        """
        Optional override.
        Return a user id from the given token.
        Return None will cause a validation error.
        """
        payload = self.resolve_token_payload(token) or {}
        user_id = payload.get('uid')
        return user_id

    def resolve_request_token(self):
        """
        Optional override.
        Return token from the request object.
        Returning None will cause an validation error.
        """
        token_header = request.headers.get('Authorization')
        token_arg = request.args.get('token')
        return token_header or token_arg

    # Advanced optional overrides

    def check_token(self, token):
        """
        Advanced/critical override.
        Returns True after passing all checks, otherwise raises.
        """

        # token - validity check
        payload = self.resolve_token_payload(token)
        if not payload:
            # raise AuthTokenError("Token invalid.")
            raise InvalidTokenError

        # token - payload: uid field check
        user_id = self.resolve_token_user_id(token)
        if not user_id:
            # raise AuthTokenError("Token 'uid' missing from payload.")
            raise InvalidTokenPayloadError

        # token - payload: custom check
        if not self.check_token_payload(payload):
            # raise AuthTokenError("Payload validation error.")
            raise InvalidTokenPayloadError

        # system - user check
        if not self.check_user_id(user_id):
            # raise AuthTokenError("Token 'uid' is invalid user.")
            raise InvalidTokenUserError

        return True

__all__ = ['AuthFlowBase']
