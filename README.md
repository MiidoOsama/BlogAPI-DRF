# Mido Blog API

A Django REST Framework project that provides a REST API for creating and
managing blog posts, with JWT authentication. The project uses SQLite by
default.

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

## Authentication

The project uses Django's built-in `auth.User` model with username-based login
and [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/) for
token authentication. Registration and logout are handled by custom views in
the `accounts` app; token blacklisting is enabled, so logout revokes the
refresh token on the server.

| Method | URL | JSON body / behavior |
| --- | --- | --- |
| `POST` | `/api/register/` | Register with `username`, `password`, and optional `email`; returns the created user plus `access` and `refresh` tokens |
| `POST` | `/api/login/` | Send `username`, `password`; returns `access` and `refresh` |
| `POST` | `/api/refresh/` | Send `refresh`; returns a new `access` |
| `POST` | `/api/logout/` | Send `refresh`; blacklists the refresh token (requires authentication) |

`/api/token/` and `/api/token/refresh/` are also available as aliases for
login and refresh.

For authenticated requests, send the access token in the header:

```
Authorization: Bearer <access-token>
```

Passwords are write-only and never included in responses. Current token
lifetimes are 15 days for access tokens and 1 day for refresh tokens.

## Posts API

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
