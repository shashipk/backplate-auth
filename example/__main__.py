
from flask import Flask
from backplate import create_api, endpoint
from backplate_auth.helpers import backplate_auth_errordefs
from auth import requires_auth_token
from endpoints import Profile, Items, Item, Auth

endpoints = [
    endpoint('me', '/me', Profile),
    endpoint('item', '/items', Items, Item),
    endpoint('auth', '/auth', Auth)
]

errors = []
errors.extend(backplate_auth_errordefs)

app = create_api(
    __name__,
    app=Flask(__name__),
    endpoints=endpoints,
    decorators=[requires_auth_token],
    errors=errors
)

if __name__ == '__main__':
    app.run(debug=True)
