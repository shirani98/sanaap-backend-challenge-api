# API Endpoints Summary

## Base Path
All endpoints are prefixed with `/api/`

## CRUD Endpoints

### Records Management

| Method | Endpoint | View | Description |
|--------|----------|------|-------------|
| GET | `/api/records/` | DataRecordListCreateView | List all records with search/filter |
| POST | `/api/records/` | DataRecordListCreateView | Create a new record |
| GET | `/api/records/<id>/` | DataRecordDetailView | Retrieve a specific record |
| PUT | `/api/records/<id>/` | DataRecordDetailView | Full update of a record |
| PATCH | `/api/records/<id>/` | DataRecordDetailView | Partial update of a record |
| DELETE | `/api/records/<id>/` | DataRecordDetailView | Delete a record |

### Filter & Status Endpoints

| Method | Endpoint | View | Description |
|--------|----------|------|-------------|
| GET | `/api/records/active/list/` | DataRecordActiveListView | List only active records |
| GET | `/api/records/inactive/list/` | DataRecordInactiveListView | List only inactive records |
| POST | `/api/records/<id>/toggle-active/` | DataRecordToggleActiveView | Toggle active status |

### Bulk Operations

| Method | Endpoint | View | Description |
|--------|----------|------|-------------|
| POST | `/api/records/bulk/delete/` | DataRecordBulkDeleteView | Delete multiple records |
| POST | `/api/records/bulk/update-status/` | DataRecordBulkUpdateStatusView | Update status for multiple records |

## Query Parameters

### List Records (`GET /api/records/`)
- `search` - Search by title or description
- `is_active` - Filter by status (true/false)
- `ordering` - Sort by field (default: `-created_at`)

### Example Requests

**Search for records:**
```bash
GET /api/records/?search=example
```

**Filter active records:**
```bash
GET /api/records/?is_active=true
```

**Sort by title:**
```bash
GET /api/records/?ordering=title
```

**Combine filters:**
```bash
GET /api/records/?search=example&is_active=true&ordering=-updated_at
```

## Response Format

### Success Responses

**2xx Status Codes:**
- `200 OK` - Successful GET, PUT, PATCH, POST (bulk operations)
- `201 Created` - Successful POST (create single resource)
- `204 No Content` - Successful DELETE

### Error Responses

**4xx Status Codes:**
- `400 Bad Request` - Validation errors, invalid parameters
- `404 Not Found` - Resource not found

**Error Response Format:**
```json
{
  "error": "Error message"
}
```

## Request/Response Examples

### Create Record
```bash
POST /api/records/
Content-Type: application/json

{
  "title": "My Record",
  "description": "A description",
  "file": null,
  "is_active": true
}
```

### Update Record (Full)
```bash
PUT /api/records/1/
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description",
  "file": null,
  "is_active": false
}
```

### Update Record (Partial)
```bash
PATCH /api/records/1/
Content-Type: application/json

{
  "title": "Only update title"
}
```

### Bulk Delete
```bash
POST /api/records/bulk/delete/
Content-Type: application/json

{
  "ids": [1, 2, 3, 4, 5]
}
```

### Bulk Update Status
```bash
POST /api/records/bulk/update-status/
Content-Type: application/json

{
  "ids": [1, 2, 3],
  "is_active": true
}
```

## Implementation Architecture

### Class Structure
- **APIView Classes:** Each view is a class-based view inheriting from `APIView`
- **Service Layer:** Business logic encapsulated in `DataRecordService`
- **Selector Layer:** Query logic encapsulated in `DataRecordSelector`
- **Serializers:** Data validation and serialization in `DataRecordSerializer`

### Flow
```
HTTP Request
    ↓
APIView (Handle HTTP method)
    ↓
Validate Input (Serializer)
    ↓
Service/Selector (Business Logic)
    ↓
Database Query
    ↓
Response (HTTP 200/201/204/400/404)
```

## Notes

- All timestamps are in ISO 8601 format
- File uploads are handled through the `file` field
- Records are ordered by creation date (newest first) by default
- Validation errors include specific error messages
- All CRUD operations respect the Service Selector pattern
