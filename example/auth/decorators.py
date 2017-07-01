
from auth.flow import flow
from backplate_auth import create_auth_decorator

requires_auth_token = create_auth_decorator(flow, whitelist=['auth'])

__all__ = ['requires_auth_token']
