# Backplate Auth

Seamlessly integrate authentication JWTs for stateless, (or revokable tokens with sessions) into your API with Backplate's authentication extension library.

```bash
$ pip install backplate-auth
```

## Features

- Sleek renewable token flow for sustained logins.
- Database agnostic auth flow method classes for subclassing.
- Remotely revokable tokens with helper session auth flow method classes.
- Highly customisable with sensible defaults.
- Allows for multiple authentication flow implementations.
- Complete endpoint and decorator generators.
- Error handling helpers for binding with `backplate`.

- [Documentation](https://github.com/studioarmix/backplate-auth/tree/master/docs)
- [Example Project App (Source)](https://github.com/studioarmix/backplate-auth/tree/master/example)

## Concept
1. Creates an endpoint that accepts a `POST` request from which it may be parsed any way to return a user id to feature in a returned JWT.
1. Creates a decorator that examines a token from the request, by default from a `Authorization` header or a `token` url query parameter, and either denies the request with a `401`, or continues the request response flow with a user object populated in the `g.user` response context.

## Quickstart

Creating a simple Flask-based API app prefixed with `/v1` with a renewable JWT token authentication flow.

### Endpoint and Decorator

The `backplate-auth` token flow works with **two main components** created to be added to `backplate.create_api` .

1. **An endpoint** to issue tokens.
2. **A decorator** to enforce the use of those tokens, and inject the user object into the response context.

Both of these components can be created with:

```python
from backplate_auth import create_auth_endpoint, create_auth_decorator

AuthResource = create_auth_endpoint(AuthTokenFlow)
auth_required = create_auth_decorator(AuthTokenFlow, whitelist=['auth'])
```

>  Note that the `whitelist` argument disables token authentication for certain endpoints by referenced by name, **it is important to declare your `auth` endpoint**, otherwise your auth flow will become a catch-22 scenario.



### AuthTokenFlow

The `backplate-auth` token flow also requires an class instance which inherits the methods of `AuthTokenFlowBase`.

```python
from backplate_auth import AuthTokenFlowBase

class AuthTokenFlow(AuthTokenFlowBase):
    # ...
```

When declaring your own subclass of `AuthTokenFlowBase` there some are methods that must be implemented, otherwise they will throw a `NotImplementedError`.



#### `resolve_request_user_id(self) => any`

Returns the token payload's user id from authentication arguments, e.g. `email` and `password`.

This would normally involve a lookup in a database.

Returning `None` will cause a validation error.

```python
# example
def resolve_request_user_id(self):
    # request arguments
    email = request.args.get('email')
    password = request.args.get('password')
    # query database for user
    user = database.user.get(email)
    # check user password
    if user and user.check_password(password):
        # success - return user id
        return user.id
    # failure - return None
    return None
```



#### `resolve_user_id(self, user_id:any) => any`

Returns a user object for `user_id` for use in the response context.

This would normally involve a lookup in a database.

Is used to bind the user's object to `flask.g` accessible with `g.user`.

Returning `None` will cause a validation error.

```python
# example
def resolve_user_id(self, user_id):
    # query database for user
    user = database.user.get(user_id)
    if user:
        # success - return user intended for g.user context
        return user
    # failure - return None
    return None
```



### Error Handling

All `backplate-auth` errors inherit `backplate_auth.exceptions.AuthError`.

From here are two error bases:

- `AuthValidationError`, raised from the `/auth` endpoint errors.
- `AuthAccessError`, raised from the decorator's validation errors when accessing protected resources without a valid token.

From here all smaller errors inherit from `AuthValidationError`:

- `AuthInvalidTokenError`, when the token structure is invalid.
- `AuthInvalidTokenPayloadError`, when the token payload structure is invalid.
- `AuthInvalidTokenUserError`, when the token structure is valid, but the user id contained within the payload fails validation.
- `AuthResolveRequestUserError`, when the payload user id could not be resolved from the request's request context, e.g. invalid email/password, OAuth flow failure etc.
- `AuthInvalidSessionError`, when the payload session handle fails validation.



#### Backplate "Errordefs" Helper

Using `backplate`'s error handling framework, simply adding `backplate_auth_errordefs` to the `create_api`'s `errors` argument can resolve any exceptions arising from token validation and associated exceptions.

```python
from backplate_auth.helpers import backplate_auth_errordefs

errors = []
errors.extend(backplate_auth_errordefs)

app = create_api(
    ...
    errors=errors,
    ...
)
```



### Configuration

Creating a JWT requires a `secret` and an `expiry` value, which can be set through config variables passed to your `Flask` app instance's `config` structure, accessed through `current_app.config`.

#### `SECRET_KEY`

A string used for signing the token's signature, defaults to `'secret'`.

#### `AUTH_TOKEN_LIFE`

A `datetime.timedelta` object used to expire the token, defaults to `weeks=1`.




### Sessions (Revokable JWTs)

In the case that you would like to make your issued JWTs revokable, `backplate-auth`  also offers an `AuthTokenSessionsBase` class that binds over your `AuthTokenFlowBase` flow class which similarly requires some methods to be implemented, otherwise they will throw a `NotImplementedError`.

```python
class AuthTokenSessions(AuthTokenSessionsBase):
    # ... session handling specific overrides

class AuthTokenFlow(AuthTokenSessions, AuthTokenFlowBase):
    # ... general handling specific overrides

# creating the endpoint and decorator
flow = AuthTokenFlow()
AuthResource = create_auth_endpoint(flow)
auth_required = create_auth_decorator(flow, whitelist=['auth'])

# ...
```



#### `check_session(self, session:any, user_id:any) => boolean`

Returns a boolean value to represent that validity of a session.

This would normally involve a lookup into some kind of session store, i.e. a database.

Returning `False` will cause a validation error.

```python
# example
def check_session(self, session, user_id):
    # query database for session by user
    db_session = database.session.where(session=session, user_id=user_id)
    if db_session:
        return True
    return False
```



#### `get_session(self, user_id:any) => any`

Returns any serialisable value to be included in the JWT, typically an integer or string to correspond as a handler for a session, which will be passed to `check_session` for validating the JWT.

Returning `None` will most probably invalidate the token.

```python
# example
def get_session(self, user_id):
    # create/commit new session
    db_session = database.session.create(user_id=user_id)
    # db_session => id = 57, user_id = 2
    return db_session.id
```

