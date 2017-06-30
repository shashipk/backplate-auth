
from functools import wraps
from flask import request, abort, g

def create_auth_decorator(AuthFlow, ignored_endpoints=[]):

    flow = AuthFlow

    def check_ignored_endpoint(endpoint):
        def trim_api_name_endpoint(endpoint):
            endpoint_parts = endpoint.split('.')
            if len(endpoint_parts) == 1:
                return endpoint
            return ''.join(endpoint_parts[1:])

        request_endpoint = trim_api_name_endpoint()
        for endpoint in ignored_endpoints:
            if request_endpoint.startswith(endpoint):
                return True

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            g.user = None

            # check if the endpoint is ignored
            if check_ignored_endpoint(request.url_rule.endpoint):
                return f(*args, **kwargs)

            # get token from header or request parameter
            token = flow.resolve_request_token()

            # validate the token,
            if flow.check_token(token):
                user_id = flow.resolve_token_user_id(token)
                g.user = flow.resolve_user_id(user_id)
                return f(*args, **kwargs)

            # 401 auth failed
            return abort(401)

        return wrapped
    return wrapper
