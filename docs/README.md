# Backplate Auth Documentation

### Configuration

Accessed through `current_app.config`.

#### `SECRET_KEY`

A string used for signing the token's signature, defaults to `'secret'`.

#### `AUTH_TOKEN_LIFE`

A `datetime.timedelta` object used to expire the token, defaults to `weeks=1`.



### Creators

#### `create_auth_endpoint(AuthTokenFlow)`

```python
from backplate_auth import create_auth_endpoint
```

Creates an endpoint that accepts a `POST` request from which it may be parsed any way to return a user id to feature in a returned JWT.



- `AuthTokenFlow`
  An class instance which inherits the methods of `AuthTokenFlowBase`.
- **Returns**
  A preconfigured subclass of `flask_restful.Resource` that handles auth requests.





#### `create_auth_decorator(AuthTokenFlow, whitelist?)`

```python
from backplate_auth import create_auth_decorator
```

Creates a decorator that examines a token from the request, by default from a `Authorization` header or a `token` url query parameter, and either denies the request with a `401`, or continues the request response flow with a user object populated in the `g.user` response context.



- `AuthTokenFlow`
  An class instance which inherits the methods of `AuthTokenFlowBase`.
- `whitelist (default = [])`
  Disables token authentication for certain endpoints by referenced by name.
- **Returns**
  A preconfigured decorator for the API that handles enforcing valid JWTs.





### Flows

#### `AuthTokenFlowBase`

```python
from backplate_auth import AuthTokenFlowBase
```

- [AuthTokenFlowBase](https://github.com/studioarmix/backplate-auth/tree/master/docs/AuthTokenFlowBase.md)



#### `AuthTokenSessionsBase`

```python
from backplate_auth import AuthTokenSessionsBase
```

- [AuthTokenSessionsBase](https://github.com/studioarmix/backplate-auth/tree/master/docs/AuthTokenSessionsBase.md)





### Helpers

#### `backplate_auth_errordefs`

```python
from backplate_auth.helpers import backplate_auth_errordefs
```

Using `backplate`'s error handling framework, simply adding `backplate_auth_errordefs` to the `create_api`'s `errors` argument can resolve any exceptions arising from token validation and associated exceptions.



```python
errors = []
errors.extend(backplate_auth_errordefs)
```



### Exceptions

```python
from backplate_auth.exceptions import ...
```

- **`AuthError => Exception`**
  Base exception.


#### General Errors

All inherit `AuthError`.

- **`AuthValidationError`**
  Raised from the `/auth` endpoint errors.
- **`AuthAccessError`**
  Raised from the decorator when accessing without valid token.



#### Validation Errors

All inherit `AuthValidationError`.

- **`AuthInvalidTokenError`**
  When the token structure is invalid.

- **`AuthInvalidTokenPayloadError`**
  When the token payload structure is invalid.

- **`AuthInvalidTokenUserError`**
  When the token structure is valid, but the payload user id fails validation.

- **`AuthResolveRequestUserError`**
  When the payload user id could not be resolved from the request's request context, e.g. invalid email/password, OAuth flow failure etc.

- **`AuthInvalidSessionError`**
  When the payload session handle fails validation.

