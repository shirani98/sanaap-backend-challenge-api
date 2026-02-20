# DMS System

A Document Management System REST API built with Django 5 and DRF.

## Stack

Django 5 · DRF · SimpleJWT · PostgreSQL · Redis · MinIO · drf-spectacular

## Quick Start (Docker)

```bash
cp .env.example .env           # configure secrets
docker compose up --build -d   # start all services
docker compose exec web python manage.py createsuperuser
```

Services: `web` · `db` (PostgreSQL) · `redis` · `minio` · `celery`

- MinIO console: `http://localhost:9001`
- API: `http://localhost:8000/api/`

## Quick Start (Local)

```bash
poetry install
cp .env.example .env           # set DATABASE_URL=sqlite:///db.sqlite3 for local dev
poetry run python manage.py migrate
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
