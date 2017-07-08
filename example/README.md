# Backplate Auth Example

#### 1. Create a virtual environment.

```
$ virtualenv -p python3 venv
```

#### 2. Install requirements.

```
$ pip install backplate backplate-auth
```

#### 3. Run.

```
$ python example
```



## Structure

Endpoints, all prefixed with `/v1`:

- `/me` - Based on auth token, will show information about the user.
- `/items` - Returns all existing items.
- `/items/:id` - Returns information on one specific item selected by `:id`.
- `/auth`
  - `POST` - (login) If posting the url query parameter `/auth?chicken` is present the endpoint will successfully authenticate and return an auth token JWT for use as either a `Authorization` header, or url query parameter `?token=...`.
  - `DELETE` - (logout) Deletes the session associated with the token, revoking that token before its expiry time.