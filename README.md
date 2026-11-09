# Mido Blog API

A Django project that provides a REST API for creating and managing blog posts.
The project uses SQLite by default.

## Authentication

The project uses Django's built-in `auth.User` model with username-based login.
The `accounts` app must not define a separate concrete `AbstractUser` subclass
while `AUTH_USER_MODEL` is set to `auth.User`, as their reverse accessors clash.

Authentication uses [Djoser](https://djoser.readthedocs.io/en/latest/authentication_backends.html)
with Simple JWT, routed through `accounts.urls`. Legacy `/auth/token/login/` and
`/auth/token/logout/` endpoints are not enabled.

| Method | URL | JSON body / behavior |
| --- | --- | --- |
| `POST` | `/auth/users/` | Register with `username`, `password`, and optional `email`, `first_name`, `last_name` |
| `POST` | `/auth/jwt/create/` | Send `username`, `password`; returns `access` and `refresh` |
| `POST` | `/auth/jwt/refresh/` | Send `refresh`; returns a new `access` |
| `POST` | `/auth/jwt/verify/` | Send `token`; returns `200 {}` if valid |
| `GET` | `/auth/users/me/` | Retrieve the authenticated account |
| `PATCH` | `/auth/users/me/` | Update account fields such as `first_name`, `last_name` |
| `POST` | `/auth/users/set_password/` | Send `current_password`, `new_password`; requires authentication |

For authenticated requests, use `Authorization: Bearer <access_token>`.
The Bearer header is retained for compatibility with existing clients rather
than the `JWT` header shown in Djoser's example. JWT login uses `username`, not
email. Passwords are validated, hashed, and never included in account responses.
An unauthenticated `GET /auth/users/` returns `401`; use `POST` to register.

There is no JWT logout endpoint in this configuration: clients sign out by
discarding their tokens, which does not revoke them on the server. Current
lifetimes are 15 days for access tokens and 1 day for refresh tokens.
Email activation and frontend password-reset links are not configured.

## Requirements

- Python
- Dependencies listed in [`requirements.txt`](requirements.txt)

## Setup

From the project directory:

```bash
python -m venv .venv
```

Activate the virtual environment, then install dependencies and initialize the
database:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The development server runs at `http://127.0.0.1:8000/`.

## API

The posts endpoints are available under `/api/`:

| Method | URL | Description |
| --- | --- | --- |
| `GET` | `/api/posts/` | List posts |
| `POST` | `/api/posts/` | Create a post |
| `GET` | `/api/posts/<id>/` | Retrieve a post |
| `PUT` / `PATCH` | `/api/posts/<id>/` | Update a post |
| `DELETE` | `/api/posts/<id>/` | Delete a post |

For example, create a post in Postman with `POST http://127.0.0.1:8000/api/posts/`,
select **Body → raw → JSON**, and send:

```json
{
  "title": "My first post",
  "content": "Hello, blog!",
  "author": 1
}
```

Use the ID of an existing user for `author`. The response contains the post's
`id`, `title`, `content`, `author`, `created_at`, and `updated_at` fields.

## Tests

Run the Django test suite with:

```bash
python manage.py test
```
