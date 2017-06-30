
import jwt
from datetime import datetime, timedelta
from flask import current_app

class JWT:

    def __init__(self, secret=None, life=None):
        """
        :param expiry:
            Timedelta <datetime.timedelta> from time of issue.
            Defaults to config key "AUTH_TOKEN_LIFE".
        :param secret:
            Secret string for signing jwt.
            Defaults to config key "SECRET_KEY".
        """

        self.secret = secret
        self.life = life

    def create(self, payload):
        """
        :param payload:
            Dictionary for token payload.
        """

        # defaults
        config = current_app.config
        secret = self.secret or config.get('SECRET_KEY') or 'secret'
        life = self.life or config.get('AUTH_TOKEN_LIFE') or timedelta(weeks=1)

        payload['exp'] = datetime.utcnow() + life
        return jwt.encode(payload, secret, algorithm='HS256').decode()

    def parse(self, token):
        """
        :param token:
            String of JWT to decode.
        """

        # defaults
        config = current_app.config
        secret = self.secret or config.get('SECRET_KEY') or 'secret'

        try:
            return jwt.decode(token, secret, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError:
            return None

__all__ = ['JWT']
