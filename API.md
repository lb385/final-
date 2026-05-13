# API Specification

## Base URL

- Development: `http://localhost:8000`
- Production: `https://yourdomain.com`

## Authentication

All endpoints except `/api/auth/register`, `/api/auth/login`, and `/health` require authentication.

### Authentication Header
```
Authorization: Bearer <access_token>
```

## Response Format

### Success Response (2xx)
```json
{
  "data": {...}
}
```

### Error Response (4xx, 5xx)
```json
{
  "detail": "Error message"
}
```

---

## Endpoints

### Authentication Endpoints

#### Register User
**Endpoint:** `POST /api/auth/register`

**Description:** Create a new user account

**Request Body:**
```json
{
  "username": "string (3-255 chars)",
  "email": "user@example.com",
  "password": "string (min 8 chars)"
}
```

**Response (200):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Error (400):**
```json
{
  "detail": "Username or email already registered"
}
```

---

#### Login User
**Endpoint:** `POST /api/auth/login`

**Description:** Authenticate user and get access token

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

**Error (401):**
```json
{
  "detail": "Invalid credentials"
}
```

---

### Profile Endpoints

#### Get Current User Profile
**Endpoint:** `GET /api/profile`

**Description:** Get authenticated user's profile information

**Authentication:** Required ✅

**Response (200):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Error (401):**
```json
{
  "detail": "Missing authorization header"
}
```

---

#### Update User Profile
**Endpoint:** `PUT /api/profile`

**Description:** Update user profile information (username and/or email)

**Authentication:** Required ✅

**Request Body:**
```json
{
  "username": "newusername (optional)",
  "email": "newemail@example.com (optional)"
}
```

**Response (200):**
```json
{
  "id": 1,
  "username": "newusername",
  "email": "newemail@example.com",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:35:00"
}
```

**Error (400):**
```json
{
  "detail": "Username already taken"
}
```

**Error (400):**
```json
{
  "detail": "Email already taken"
}
```

---

#### Change Password
**Endpoint:** `POST /api/profile/change-password`

**Description:** Change user password

**Authentication:** Required ✅

**Request Body:**
```json
{
  "old_password": "string",
  "new_password": "string (min 8 chars)",
  "confirm_password": "string (must match new_password)"
}
```

**Response (200):**
```json
{
  "message": "Password changed successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:40:00"
  }
}
```

**Error (401):**
```json
{
  "detail": "Old password is incorrect"
}
```

**Error (400):**
```json
{
  "detail": "New passwords do not match"
}
```

---

### Health Endpoint

#### Health Check
**Endpoint:** `GET /health`

**Description:** Check if server is running

**Authentication:** Not required ✓

**Response (200):**
```json
{
  "status": "healthy"
}
```

---

## Data Models

### User Model
```
id          : integer (primary key)
username    : string (unique, 3-255 chars)
email       : string (unique, valid email format)
password_hash : string (bcrypt hash)
created_at  : datetime
updated_at  : datetime
```

### Calculation Model
```
id        : integer (primary key)
user_id   : integer (foreign key → User)
operand1  : float
operand2  : float
operation : string
result    : float
created_at: datetime
```

---

## HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful request |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing/invalid token |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Username already exists |
| 500 | Server Error | Database error |

---

## Request/Response Examples

### Example 1: Register and Login

**Step 1: Register**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Step 2: Login**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

---

### Example 2: Update Profile

```bash
curl -X PUT http://localhost:8000/api/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "email": "john.new@example.com"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john.new@example.com",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:35:00"
}
```

---

### Example 3: Change Password

```bash
curl -X POST http://localhost:8000/api/profile/change-password \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "old_password": "SecurePassword123",
    "new_password": "NewSecurePassword456",
    "confirm_password": "NewSecurePassword456"
  }'
```

**Response:**
```json
{
  "message": "Password changed successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john.new@example.com",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:40:00"
  }
}
```

---

## Rate Limiting

Currently not implemented. Can be added with:
- FastAPI SlowAPI
- Redis-based limiting
- Database-backed tracking

---

## CORS Configuration

**Allowed Origins:** `*` (all origins in development)

**Allowed Methods:** `GET, POST, PUT, DELETE, OPTIONS`

**Allowed Headers:** `Content-Type, Authorization`

For production, restrict to specific domains:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    ...
)
```

---

## Token Expiration

- **Access Token Lifetime:** 30 minutes (configurable)
- **Refresh Token:** Not implemented (future enhancement)

---

## Validation Rules

### Username
- Minimum length: 3 characters
- Maximum length: 255 characters
- Must be unique
- Allowed characters: alphanumeric, underscore, hyphen

### Email
- Must be valid email format
- Must be unique
- No length restrictions

### Password
- Minimum length: 8 characters
- No maximum length
- No complexity requirements (can be added)
- Stored as bcrypt hash (never stored plain text)

---

## Error Handling

### Common Errors

**401 Unauthorized**
```json
{
  "detail": "Invalid token"
}
```

**400 Bad Request**
```json
{
  "detail": "Value error, string should match regex"
}
```

**500 Internal Server Error**
```json
{
  "detail": "Internal server error"
}
```

---

## API Documentation

### Interactive Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

---

## Future API Enhancements

- [ ] Pagination for list endpoints
- [ ] Filtering and sorting
- [ ] Rate limiting
- [ ] Webhook support
- [ ] Batch operations
- [ ] GraphQL endpoint
- [ ] API versioning
- [ ] Request signing

---

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release
- User authentication
- Profile management
- Password change

---

**Last Updated:** 2026-05-12
**API Version:** 1.0.0
