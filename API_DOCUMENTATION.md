# Task Management API - Complete Documentation

**Version:** 1.0.0  
**Author:** Benjamin Emeshili (101004677)  
**Last Updated:** April 1, 2026  

---

## Table of Contents

1. [Overview](#overview)
2. [Base URLs](#base-urls)
3. [Authentication](#authentication)
4. [Quick Start](#quick-start)
5. [API Endpoints](#api-endpoints)
6. [Data Models](#data-models)
7. [Error Handling](#error-handling)
8. [Rate Limits](#rate-limits)
9. [Security](#security)
10. [Examples](#examples)

---

## Overview

The Task Management API is a RESTful web service that allows users to manage tasks with full CRUD (Create, Read, Update, Delete) operations. The API features JWT-based authentication, user isolation, and comprehensive input validation.

### Key Features

- ✅ User registration and authentication
- ✅ JWT token-based security
- ✅ Full CRUD operations on tasks
- ✅ Task filtering by status, priority, and category
- ✅ User data isolation
- ✅ Bcrypt password hashing
- ✅ SQLite database persistence
- ✅ Input validation on all endpoints

### Technology Stack

- **Framework:** Flask 3.0.0
- **Database:** SQLite with SQLAlchemy ORM
- **Authentication:** JWT (Flask-JWT-Extended 4.6.0)
- **Password Hashing:** Bcrypt
- **Language:** Python 3.13

---

## Base URLs

### Production Environment
https://api-production-bb06.up.railway.app
**Use for:** Production applications, live demos, final testing

### Development Environment
https://api-production-3ebb.up.railway.app
**Use for:** Development, experimental features, initial testing

### Health Check
Both environments provide a health check endpoint:
```bash
GET /health
Response: {"status": "healthy"}
```

---

## Authentication

### Overview

The API uses JWT (JSON Web Tokens) for authentication. After successful login, you receive a token that must be included in the `Authorization` header for all protected endpoints.

### Authentication Flow

Register User → POST /api/auth/register
Login → POST /api/auth/login → Receive JWT Token
Use Token → Include in Authorization header for all requests
Token Expires → Login again to get new token (1 hour expiry)


### Using Authentication Tokens


**Example:**
```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  https://api-production-bb06.up.railway.app/api/tasks
```

### Token Expiration

- **Default Expiry:** 1 hour from creation
- **Renewal:** Login again to obtain a new token
- **Best Practice:** Store token securely, refresh before expiry

---

## Quick Start

### 1. Register a New User
```bash
curl -X POST https://api-production-bb06.up.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securePassword123"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2026-04-01T10:30:00"
}
```

### 2. Login
```bash
curl -X POST https://api-production-bb06.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securePassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2026-04-01T10:30:00"
  }
}
```

**💡 Save the `access_token` - you'll need it for all subsequent requests!**

### 3. Create Your First Task
```bash
curl -X POST https://api-production-bb06.up.railway.app/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Complete API documentation",
    "description": "Write comprehensive API docs",
    "priority": "high",
    "status": "in_progress",
    "category": "work"
  }'
```

### 4. Get All Your Tasks
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  https://api-production-bb06.up.railway.app/api/tasks
```

---

## API Endpoints

### Summary Table

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/health` | ❌ No | Health check |
| POST | `/api/auth/register` | ❌ No | Register new user |
| POST | `/api/auth/login` | ❌ No | Login and get token |
| GET | `/api/tasks` | ✅ Yes | Get all tasks (filterable) |
| POST | `/api/tasks` | ✅ Yes | Create new task |
| GET | `/api/tasks/{id}` | ✅ Yes | Get specific task |
| PUT | `/api/tasks/{id}` | ✅ Yes | Update task |
| DELETE | `/api/tasks/{id}` | ✅ Yes | Delete task |

---

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running

**Authentication:** Not required

**Request:**
```bash
curl https://api-production-bb06.up.railway.app/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200 OK` - API is running

---

### 2. Register User

**Endpoint:** `POST /api/auth/register`

**Description:** Create a new user account

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "string (required, unique)",
  "email": "string (required, unique, valid email)",
  "password": "string (required, min 6 characters recommended)"
}
```

**Example Request:**
```bash
curl -X POST https://api-production-bb06.up.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "alicePass123"
  }'
```

**Success Response (201 Created):**
```json
{
  "id": 2,
  "username": "alice",
  "email": "alice@example.com",
  "created_at": "2026-04-01T14:22:00"
}
```

**Error Responses:**

| Status Code | Error | Description |
|-------------|-------|-------------|
| 400 | `Missing required fields` | username, email, or password not provided |
| 400 | `Username already exists` | Username is taken |
| 400 | `Email already exists` | Email is already registered |
| 400 | `Invalid JSON` | Request body is not valid JSON |

**Example Error:**
```json
{
  "error": "Username already exists"
}
```

---

### 3. Login

**Endpoint:** `POST /api/auth/login`

**Description:** Authenticate user and receive JWT token

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**Example Request:**
```bash
curl -X POST https://api-production-bb06.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "alicePass123"
  }'
```

**Success Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MzY5ODgwMCwianRpIjoiYjk4ZDYzYTYtYWQ2ZC00ZmU4LWIzNDYtZTg5ZGE4NWM3YzRjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE2NDM2OTg4MDAsImV4cCI6MTY0MzcwMjQwMH0.xK3y7YlqL9zQ1pRj8vNmC2aS4bT6wE9hU0iO5jK7lMn",
  "user": {
    "id": 2,
    "username": "alice",
    "email": "alice@example.com",
    "created_at": "2026-04-01T14:22:00"
  }
}
```

**Error Responses:**

| Status Code | Error | Description |
|-------------|-------|-------------|
| 400 | `Missing username or password` | Required fields not provided |
| 401 | `Invalid credentials` | Username or password is incorrect |
| 400 | `Invalid JSON` | Request body is not valid JSON |

---

### 4. Get All Tasks

**Endpoint:** `GET /api/tasks`

**Description:** Retrieve all tasks for the authenticated user with optional filtering

**Authentication:** Required (JWT token)

**Query Parameters:**

| Parameter | Type | Description | Values |
|-----------|------|-------------|--------|
| `status` | string | Filter by status | `todo`, `in_progress`, `done` |
| `priority` | string | Filter by priority | `low`, `medium`, `high` |
| `category` | string | Filter by category | Any string value |

**Example Requests:**

**Get all tasks:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api-production-bb06.up.railway.app/api/tasks
```

**Get only high-priority tasks:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api-production-bb06.up.railway.app/api/tasks?priority=high"
```

**Get tasks that are in progress:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api-production-bb06.up.railway.app/api/tasks?status=in_progress"
```

**Multiple filters (in progress AND high priority):**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api-production-bb06.up.railway.app/api/tasks?status=in_progress&priority=high"
```

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Complete API documentation",
    "description": "Write comprehensive API docs",
    "status": "in_progress",
    "priority": "high",
    "category": "work",
    "due_date": "2026-04-10T00:00:00",
    "created_at": "2026-04-01T10:00:00",
    "updated_at": "2026-04-01T15:30:00",
    "user_id": 2
  },
  {
    "id": 2,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "todo",
    "priority": "medium",
    "category": "personal",
    "due_date": null,
    "created_at": "2026-04-01T11:00:00",
    "updated_at": "2026-04-01T11:00:00",
    "user_id": 2
  }
]
```

**Empty Response (200 OK):**
```json
[]
```

**Error Responses:**

| Status Code | Error | Description |
|-------------|-------|-------------|
| 401 | `Missing Authorization Header` | No JWT token provided |
| 422 | `Invalid token` | JWT token is malformed or expired |

---

### 5. Create Task

**Endpoint:** `POST /api/tasks`

**Description:** Create a new task for the authenticated user

**Authentication:** Required (JWT token)

**Request Body:**
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "status": "string (optional, default: 'todo')",
  "priority": "string (optional, default: 'medium')",
  "category": "string (optional)",
  "due_date": "ISO 8601 datetime string (optional)"
}
```

**Field Validation:**
- `status`: Must be one of: `todo`, `in_progress`, `done`
- `priority`: Must be one of: `low`, `medium`, `high`
- `due_date`: Must be valid ISO 8601 format (e.g., `2026-04-15T14:30:00`)

**Example Request:**
```bash
curl -X POST https://api-production-bb06.up.railway.app/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Implement user authentication",
    "description": "Add JWT-based auth to the API",
    "priority": "high",
    "status": "todo",
    "category": "development",
    "due_date": "2026-04-15T17:00:00"
  }'
```

**Minimal Request:**
```bash
curl -X POST https://api-production-bb06.up.railway.app/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Quick task"
  }'
```

**Success Response (201 Created):**
```json
{
  "id": 3,
  "title": "Implement user authentication",
  "description": "Add JWT-based auth to the API",
  "status": "todo",
  "priority": "high",
  "category": "development",
  "due_date": "2026-04-15T17:00:00",
  "created_at": "2026-04-01T16:00:00",
  "updated_at": "2026-04-01T16:00:00",
  "user_id": 2
}
```

**Error Responses:**

| Status Code | Error | Description |
|-------------|-------|-------------|
| 400 | `Title is required` | No title provided |
| 400 | `Invalid status` | Status not in allowed values |
| 400 | `Invalid priority` | Priority not in allowed values |
| 400 | `Invalid due_date format` | Date not in ISO 8601 format |
| 401 | `Missing Authorization Header` | No JWT token provided |

---

### 6. Get Single Task

**Endpoint:** `GET /api/tasks/{id}`

**Description:** Retrieve a specific task by ID (must belong to authenticated user)

**Authentication:** Required (JWT token)

**URL Parameters:**
- `id` (integer): Task ID

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api-production-bb06.up.railway.app/api/tasks/3
```

**Success Response (200 OK):**
```json
{
  "id": 3,
  "title": "Implement user authentication",
  "description": "Add JWT-based auth to the API",
  "status": "todo",
  "priority": "high",
  "category": "development",
  "due_date": "2026-04-15T17:00:00",
  "created_at": "2026-04-01T16:00:00",
  "updated_at": "2026-04-01T16:00:00",
  "user_id": 2
}
```

**Error Responses:**

| Status Code | Error | Description |
|-------------|-------|-------------|
| 404 | `Task not found` | Task doesn't exist or belongs to different user |
| 401 | `Missing Authorization Header` | No JWT token provided |

---

### 7. Update Task

**Endpoint:** `PUT /api/tasks/{id}`

**Description:** Update an existing task (must belong to authenticated user)

**Authentication:** Required (JWT token)

**URL Parameters:**
- `id` (integer): Task ID

**Request Body:** (all fields optional, only include fields you want to update)
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "status": "string (optional)",
  "priority": "string (optional)",
  "category": "string (optional)",
  "due_date": "ISO 8601 datetime string or null (optional)"
}
```

**Example Request - Update status:**
```bash
curl -X PUT https://api-production-bb06.up.railway.app/api/tasks/3 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "status": "in_progress"
  }'
```

**Example Request - Update multiple fields:**
```bash
curl -X PUT https://api-production-bb06.up.railway.app/api/tasks/3 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "status": "done",
    "priority": "low",
    "description": "Completed successfully!"
  }'
```

**Example Request - Remove due date:**
```bash
curl -X PUT https://api-production-bb06.up.railway.app/api/tasks/3 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "due_date": null
  }'
```

**Success Response (200 OK):**
```json
{
  "id": 3,
  "title": "Implement user authentication",
  "description": "Completed successfully!",
  "status": "done",
  "priority": "low",
  "category": "development",
  "due_date": null,
  "created_at": "2026-04-01T16:00:00",
  "updated_at": "2026-04-01T18:30:00",
  "user_id": 2
}
```

**Error Responses:**

| Status Code | Error | Description |
|-------------|-------|-------------|
| 400 | `Invalid status` | Status not in allowed values |
| 400 | `Invalid priority` | Priority not in allowed values |
| 400 | `Invalid due_date format` | Date not in ISO 8601 format |
| 404 | `Task not found` | Task doesn't exist or belongs to different user |
| 401 | `Missing Authorization Header` | No JWT token provided |

---

### 8. Delete Task

**Endpoint:** `DELETE /api/tasks/{id}`

**Description:** Delete a specific task (must belong to authenticated user)

**Authentication:** Required (JWT token)

**URL Parameters:**
- `id` (integer): Task ID

**Example Request:**
```bash
curl -X DELETE https://api-production-bb06.up.railway.app/api/tasks/3 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Success Response (200 OK):**
```json
{
  "message": "Task deleted"
}
```

**Error Responses:**

| Status Code | Error | Description |
|-------------|-------|-------------|
| 404 | `Task not found` | Task doesn't exist or belongs to different user |
| 401 | `Missing Authorization Header` | No JWT token provided |

---

## Data Models

### User Model
```json
{
  "id": "integer (auto-generated)",
  "username": "string (unique, required)",
  "email": "string (unique, required)",
  "created_at": "datetime (ISO 8601 format)"
}
```

**Note:** Password is never returned in responses (stored as bcrypt hash)

**Database Schema:**
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

### Task Model
```json
{
  "id": "integer (auto-generated)",
  "title": "string (required)",
  "description": "string (optional)",
  "status": "enum (todo|in_progress|done, default: todo)",
  "priority": "enum (low|medium|high, default: medium)",
  "category": "string (optional)",
  "due_date": "datetime (ISO 8601 format, optional)",
  "created_at": "datetime (ISO 8601 format, auto-generated)",
  "updated_at": "datetime (ISO 8601 format, auto-updated)",
  "user_id": "integer (foreign key to User)"
}
```

**Database Schema:**
```sql
CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'todo',
    priority VARCHAR(20) DEFAULT 'medium',
    category VARCHAR(100),
    due_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
);
```

---

## Error Handling

### Standard Error Response Format

All errors return a JSON object with an `error` field:
```json
{
  "error": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Name | Description |
|------|------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource successfully created |
| 400 | Bad Request | Invalid input or validation error |
| 401 | Unauthorized | Missing or invalid authentication token |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | JWT token validation failed |
| 500 | Internal Server Error | Server-side error |

### Common Error Scenarios

#### Missing Authentication
```json
{
  "msg": "Missing Authorization Header"
}
```

#### Invalid Token
```json
{
  "msg": "Invalid token"
}
```

#### Validation Errors
```json
{
  "error": "Title is required"
}
```
```json
{
  "error": "Invalid status. Must be one of: todo, in_progress, done"
}
```

#### Resource Not Found
```json
{
  "error": "Task not found"
}
```

---

## Rate Limits

**Current Implementation:** No rate limiting

**Recommended for Production:**
- 100 requests per minute per user
- 1000 requests per hour per user
- 10 registration attempts per IP per hour

**Future Implementation:** Will return `429 Too Many Requests` with:
```json
{
  "error": "Rate limit exceeded. Please try again later.",
  "retry_after": 60
}
```

---

## Security

### Password Security
- **Hashing Algorithm:** bcrypt with automatic salt generation
- **Minimum Length:** No enforced minimum (recommended: 8+ characters)
- **Storage:** Only bcrypt hashes stored, never plaintext

### JWT Token Security
- **Algorithm:** HS256 (HMAC with SHA-256)
- **Expiration:** 1 hour from creation
- **Secret Key:** 32+ character random string (environment variable)
- **Claims:** User ID stored as subject (`sub`)

### User Isolation
- All task endpoints enforce user ownership
- Users can only access their own tasks
- Foreign key relationships enforced at database level

### SQL Injection Protection
- SQLAlchemy ORM used for all database queries
- Parameterized queries prevent injection attacks

### HTTPS Enforcement
- Production API requires HTTPS
- All data encrypted in transit

### Input Validation
- All required fields validated
- Enum values strictly checked
- Email format validated
- Date format validated

---

## Examples

### Complete Workflow Example
```bash
# 1. Register
curl -X POST https://api-production-bb06.up.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"developer","email":"dev@example.com","password":"dev123"}'

# Response: {"id":5,"username":"developer","email":"dev@example.com",...}

# 2. Login
curl -X POST https://api-production-bb06.up.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"developer","password":"dev123"}'

# Response: {"access_token":"eyJ0eXAi...","user":{...}}
# Save the token!

# 3. Create high-priority task
TOKEN="eyJ0eXAi..."
curl -X POST https://api-production-bb06.up.railway.app/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title":"Fix production bug",
    "priority":"high",
    "status":"in_progress",
    "category":"bugs"
  }'

# Response: {"id":10,"title":"Fix production bug",...}

# 4. Get all high-priority tasks
curl -H "Authorization: Bearer $TOKEN" \
  "https://api-production-bb06.up.railway.app/api/tasks?priority=high"

# 5. Mark task as complete
curl -X PUT https://api-production-bb06.up.railway.app/api/tasks/10 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":"done"}'

# 6. Get all completed tasks
curl -H "Authorization: Bearer $TOKEN" \
  "https://api-production-bb06.up.railway.app/api/tasks?status=done"

# 7. Delete the task
curl -X DELETE https://api-production-bb06.up.railway.app/api/tasks/10 \
  -H "Authorization: Bearer $TOKEN"

# Response: {"message":"Task deleted"}
```

### JavaScript/Fetch Example
```javascript
// Base URL
const API_URL = 'https://api-production-bb06.up.railway.app';

// 1. Register
async function register() {
  const response = await fetch(`${API_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'jsuser',
      email: 'js@example.com',
      password: 'jspass123'
    })
  });
  return response.json();
}

// 2. Login
async function login() {
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'jsuser',
      password: 'jspass123'
    })
  });
  const data = await response.json();
  return data.access_token;
}

// 3. Create Task
async function createTask(token) {
  const response = await fetch(`${API_URL}/api/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      title: 'Learn API integration',
      priority: 'medium',
      status: 'todo'
    })
  });
  return response.json();
}

// 4. Get All Tasks
async function getTasks(token) {
  const response = await fetch(`${API_URL}/api/tasks`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
}

// 5. Update Task
async function updateTask(token, taskId) {
  const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ status: 'done' })
  });
  return response.json();
}

// Usage
(async () => {
  await register();
  const token = await login();
  const task = await createTask(token);
  const tasks = await getTasks(token);
  await updateTask(token, task.id);
})();
```

### Python Requests Example
```python
import requests

API_URL = 'https://api-production-bb06.up.railway.app'

# 1. Register
def register():
    response = requests.post(f'{API_URL}/api/auth/register', json={
        'username': 'pythonuser',
        'email': 'python@example.com',
        'password': 'python123'
    })
    return response.json()

# 2. Login
def login():
    response = requests.post(f'{API_URL}/api/auth/login', json={
        'username': 'pythonuser',
        'password': 'python123'
    })
    data = response.json()
    return data['access_token']

# 3. Create Task
def create_task(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(
        f'{API_URL}/api/tasks',
        json={
            'title': 'Automate testing',
            'priority': 'high',
            'status': 'todo',
            'category': 'automation'
        },
        headers=headers
    )
    return response.json()

# 4. Get Tasks
def get_tasks(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{API_URL}/api/tasks', headers=headers)
    return response.json()

# Usage
if __name__ == '__main__':
    register()
    token = login()
    task = create_task(token)
    tasks = get_tasks(token)
    print(f'Created task: {task}')
    print(f'All tasks: {tasks}')
```

---

## Support & Contact

**Project Repository:** https://github.com/styl3s/ci-cd-project  
**Author:** Benjamin Emeshili (101004677)  
**Course:** CI/CD Pipeline Implementation  
**Date:** April 2026

**For Issues:**
- Open an issue on GitHub
- Check existing documentation
- Review test cases for examples

---

**End of Documentation**

*Last Updated: April 1, 2026*  
*API Version: 1.0.0*