# API Reference

Base URL: `/api/`
Auth header: `Authorization: Bearer <access_token>`

## Auth

| Method | URL | Permission | Description |
|--------|-----|-----------|-------------|
| POST | `/auth/login/` | Public | Get access + refresh tokens |
| POST | `/auth/token/refresh/` | Public | Refresh access token |
| POST | `/auth/logout/` | Authenticated | Blacklist refresh token |

**Login request/response:**
```json
// POST /api/auth/login/
{ "username": "alice", "password": "secret" }

// 200
{ "success": true, "data": { "access": "...", "refresh": "...", "user": { "id": 1, "username": "alice", "email": "..." } } }
```

---

## Records

| Method | URL | Role | Description |
|--------|-----|------|-------------|
| GET | `/records/` | viewer + | List with filter & pagination |
| POST | `/records/create/` | editor + | Create record |
| GET | `/records/<id>/` | viewer + | Retrieve record |
| PATCH | `/records/<id>/update/` | editor + | Partial update |
| DELETE | `/records/<id>/delete/` | admin | Delete record |

### List query params
| Param | Example | Description |
|-------|---------|-------------|
| `search` | `?search=report` | Title / description match |
| `is_active` | `?is_active=true` | Filter by status |
| `created_at_after` | `?created_at_after=2025-01-01` | Date range (from) |
| `created_at_before` | `?created_at_before=2025-12-31` | Date range (to) |
| `ordering` | `?ordering=-created_at` | Sort field |
| `page` | `?page=2` | Page number |
| `page_size` | `?page_size=20` | Results per page (max 100) |

### Standard response shape
```json
{ "success": true, "message": "...", "data": { ... } }
```

### Error response shape
```json
{ "success": false, "message": "...", "errors": { ... } }
```
