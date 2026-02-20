# DataRecord API Documentation

## APIView-based CRUD Implementation

This API provides complete CRUD operations for managing data records using Django REST Framework's APIView classes with a Service Selector pattern.

### Base URL
```
/api/
```

## Endpoints

### 1. List and Create Records
**URL:** `/api/records/`

#### GET - List All Records
Retrieve all records with optional filtering and search.

**Query Parameters:**
- `search` (optional): Search by title or description
- `is_active` (optional): Filter by status (true/false)
- `ordering` (optional): Order by field (default: `-created_at`)

**Example Request:**
```bash
GET /api/records/?search=title&is_active=true&ordering=-created_at
```

**Response (200 OK):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "title": "Record 1",
      "description": "Description",
      "file": null,
      "created_at": "2026-02-20T12:00:00Z",
      "updated_at": "2026-02-20T12:00:00Z",
      "is_active": true
    }
  ]
}
```

#### POST - Create New Record
Create a new data record.

**Request Body:**
```json
{
  "title": "New Record",
  "description": "Optional description",
  "file": null,
  "is_active": true
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "New Record",
  "description": "Optional description",
  "file": null,
  "created_at": "2026-02-20T12:00:00Z",
  "updated_at": "2026-02-20T12:00:00Z",
  "is_active": true
}
```

### 2. Retrieve, Update, Delete Records
**URL:** `/api/records/<id>/`

#### GET - Retrieve Record by ID
Retrieve a specific record.

**Example Request:**
```bash
GET /api/records/1/
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Record 1",
  "description": "Description",
  "file": null,
  "created_at": "2026-02-20T12:00:00Z",
  "updated_at": "2026-02-20T12:00:00Z",
  "is_active": true
}
```

#### PUT - Full Update
Update all fields of a record.

**Request Body:**
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "file": null,
  "is_active": false
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Updated Title",
  "description": "Updated description",
  "file": null,
  "created_at": "2026-02-20T12:00:00Z",
  "updated_at": "2026-02-20T12:00:00Z",
  "is_active": false
}
```

#### PATCH - Partial Update
Update specific fields of a record.

**Request Body:**
```json
{
  "title": "Updated Title"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Updated Title",
  "description": "Description",
  "file": null,
  "created_at": "2026-02-20T12:00:00Z",
  "updated_at": "2026-02-20T12:00:00Z",
  "is_active": true
}
```

#### DELETE - Delete Record
Delete a specific record.

**Response (204 No Content)**

### 3. Active Records
**URL:** `/api/records/active/list/`

#### GET - List Active Records
Retrieve only active records.

**Response (200 OK):**
```json
{
  "count": 3,
  "results": [...]
}
```

### 4. Inactive Records
**URL:** `/api/records/inactive/list/`

#### GET - List Inactive Records
Retrieve only inactive records.

**Response (200 OK):**
```json
{
  "count": 2,
  "results": [...]
}
```

### 5. Toggle Active Status
**URL:** `/api/records/<id>/toggle-active/`

#### POST - Toggle Active Status
Toggle the is_active status of a record.

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Record 1",
  "description": "Description",
  "file": null,
  "created_at": "2026-02-20T12:00:00Z",
  "updated_at": "2026-02-20T12:00:00Z",
  "is_active": false
}
```

### 6. Bulk Delete
**URL:** `/api/records/bulk/delete/`

#### POST - Delete Multiple Records
Delete multiple records by their IDs.

**Request Body:**
```json
{
  "ids": [1, 2, 3]
}
```

**Response (200 OK):**
```json
{
  "message": "3 record(s) deleted successfully",
  "deleted_count": 3
}
```

### 7. Bulk Update Status
**URL:** `/api/records/bulk/update-status/`

#### POST - Update Status for Multiple Records
Update the is_active status for multiple records.

**Request Body:**
```json
{
  "ids": [1, 2, 3],
  "is_active": true
}
```

**Response (200 OK):**
```json
{
  "message": "3 record(s) updated successfully",
  "updated_count": 3,
  "is_active": true
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Title cannot be empty"
}
```

### 404 Not Found
```json
{
  "error": "Record not found"
}
```

## Implementation Details

### Architecture
- **Views:** APIView-based class-based views for explicit control
- **Services:** Encapsulate business logic for write operations
- **Selectors:** Encapsulate read/query logic
- **Serializers:** Handle data serialization/deserialization

### Service Selector Pattern
- **Selectors**: Handle READ operations only
- **Services**: Handle CREATE, UPDATE, DELETE operations with validation
- **Views**: Orchestrate requests to services/selectors

### Benefits
- Clear separation of concerns
- Reusable business logic
- Centralized validation
- Easier testing and maintenance
