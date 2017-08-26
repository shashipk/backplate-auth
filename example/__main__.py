
from flask import Flask
from backplate import create_api, Route
from backplate_auth.helpers import backplate_auth_errordefs
from auth import requires_auth_token
from endpoints import Profile, Items, Item, Auth

routes = [
    Route('me', '/me', Profile),
    Route('item', '/items', Items, Item),
    Route('auth', '/auth', Auth)
]

errors = []
errors.extend(backplate_auth_errordefs)

app = create_api(
    __name__,
    app=Flask(__name__),
    routes=routes,
    decorators=[requires_auth_token],
    errors=errors
)

if __name__ == '__main__':
    app.run(debug=True)
