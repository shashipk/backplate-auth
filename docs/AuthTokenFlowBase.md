# AuthTokenFlowBase

```python
from backplate_auth import AuthTokenFlowBase
```

#### Types

- `UID`
  Refers to the type that you may implement for user ids, typically `int | string`.



### Required Overrides

#### `resolve_request_user_id(self) => UID`

```
Return a user id from the request object.
Returning None will cause a validation error.
```

#### `resolve_user_id(self, user_id:UID) => any`

```
Return an object that represents the user from database user_id.
Returning None will cause a validation error.
```



### Optional Overrides

#### `new_token(self, user_id:UID) => any`

```
Return token from result of create_token_payload.
Returning anything else will cause a token creation error.
```

#### `renew_token(self, token:string) => string`

```
Return token from result of get_token_payload.
Returning anything else will cause a token creation error.
```

#### `create_token_payload(self, user_id:UID) => dict`

```
Return a dictionary containing at least the 'uid' of user.
Returning anything else will cause a token creation error.
```

#### `check_token_payload(self, payload:dict) => boolean`

```
Return a boolean after running additional validation checks.
Returning False will cause a validation error.
```

#### `get_token_payload(self, token:string) => dict`

```
Return a dictionary from the given token payload.
Returning None will cause a validation error.
```

#### `get_token_user_id(self, token:string) => UID`

```
Return a user id from the given token.
Returning None will cause a validation error.
```

#### `get_request_token(self) => string`

```
Return token from the request object.
Returning None will cause a validation error.
```



### Core Overrides

> Note that these functions contain a lot of core logic for the the flow.

#### `check_token(self, token:string) => boolean`

```
Returns True after passing all checks, otherwise raises exceptions.
Returning False will cause a validation error.
```

