# DMS System

A Document Management System REST API built with Django 5 and DRF.

## Stack

Django 5 · DRF · SimpleJWT · PostgreSQL · Redis · MinIO · drf-spectacular

## Quick Start

```bash
# Install dependencies
poetry install

# Apply migrations
poetry run python manage.py migrate

# Create superuser
poetry run python manage.py createsuperuser

# Run server
poetry run python manage.py runserver
```

Role groups (admin, editor, viewer) are created automatically on `migrate`.

## Docs

- API reference: [`docs/api.md`](docs/api.md)
- Architecture: [`docs/architecture.md`](docs/architecture.md)
- Swagger UI: `http://localhost:8000/api/docs/`

## RBAC

| Role | Create | Update | Delete | View |
|------|:------:|:------:|:------:|:----:|
| admin | ✅ | ✅ | ✅ | ✅ |
| editor | ✅ | ✅ | ❌ | ✅ |
| viewer | ❌ | ❌ | ❌ | ✅ |

## Testing

```bash
poetry run python manage.py test apps
```
