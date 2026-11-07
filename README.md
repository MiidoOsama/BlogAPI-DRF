# Mido Blog API

A Django project that provides a REST API for creating and managing blog posts.
The project uses SQLite by default.

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
