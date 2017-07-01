
class AuthError(Exception):
    pass

class AuthInvalidTokenError(AuthError):
    pass

class AuthInvalidTokenPayloadError(AuthError):
    pass

class AuthInvalidTokenUserError(AuthError):
    pass

class AuthResolveRequestUserError(AuthError):
    pass

class AuthAccessError(AuthError):
    pass

__all__ = [
    'AuthError',
    'AuthInvalidTokenError',
    'AuthInvalidTokenPayloadError',
    'AuthInvalidTokenUserError',
    'AuthResolveRequestUserError',
    'AuthAccessError'
]
