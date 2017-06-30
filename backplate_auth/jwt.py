
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

        config = current_app.config
        self.secret = secret or config.get('SECRET_KEY', 'secret')
        self.life = life or config.get('AUTH_TOKEN_LIFE', timedelta(weeks=1))

    def create(self, payload):
        """
        :param payload:
            Dictionary for token payload.
        """

        payload['exp'] = datetime.utcnow() + self.life
        return jwt.encode(payload, self.secret, algorithm='HS256').decode()

    def parse(self, token):
        """
        :param token:
            String of JWT to decode.
        """

        try:
            return jwt.decode(token, self.secret, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError:
            return None

__all__ = ['JWT']
