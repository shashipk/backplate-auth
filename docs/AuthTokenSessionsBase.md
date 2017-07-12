# AuthTokenSessionsBase

```python
from backplate_auth import AuthTokenFlowBase
```

#### Types

- `UID`
  Refers to the type that you may implement for user ids, typically `int`.
- `SSN`
  Refers to the type that you may implement for sessions, typically `int | string`.



### Required Overrides

#### `check_session(self, session: SSN, user_id: UID) => boolean`

```
Return boolean after checking session with database.
Returning False will cause a validation error.
```

#### `get_session(self, user_id: UID) => SSN`

```
Return int or string token to correspond as a handler for a session.
Returning None will most probably invalidate the token.
```



### Optional Overrides

#### `get_token_session(self, token: string) => SSN`

```
Returns session from the given token.
Returning None may cause errors.
```

#### `check_token_payload_session(self, payload: dict) => boolean`

```
Returns True after passing all checks, otherwises raises.
Returning False will cause a validation error.
```

#### `create_token_payload_session(self, payload: dict, session: SSN) => dict`

```
Returns payload dictionary after injecting the session.
```



### Core Overrides

> Note that these functions bind over methods that `AuthTokenFlowBase` expose to enable the methods implemented by `AuthTokenSessionsBase` to function.

#### `check_token_payload(self, payload: dict) => boolean`

```
Modular override that binds over AuthFlowBase.check_token_payload.
Helper override to mount check_token_payload_session to AuthFlowBase.
```

#### `create_token_payload(self, user_id: UID) => dict`

```
Modular override that bind over AuthFlowBase.create_token_payload.
Helper override to inject session into payload.
```

