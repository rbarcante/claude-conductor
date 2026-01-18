---
name: api-design
description: Use this skill when designing or implementing REST APIs, endpoints, routes, or controllers.
version: 1.0.0
---

# API Design

Guidance for designing and implementing RESTful APIs. Covers URL conventions, HTTP methods, error handling, versioning, and common patterns.

## Core Principles

1. **Resources over actions**: URLs represent resources, not operations
2. **HTTP methods for operations**: GET reads, POST creates, PUT/PATCH updates, DELETE removes
3. **Consistent error responses**: Standardized error format across all endpoints
4. **Versioning from day one**: Plan for API evolution
5. **Stateless design**: Each request contains all needed information

## REST URL Conventions

### Resource Naming

```
# Good - plural nouns, lowercase, hyphens
GET    /api/v1/users
GET    /api/v1/users/:id
GET    /api/v1/users/:id/orders
GET    /api/v1/order-items

# Avoid - verbs, mixed case, underscores
GET    /api/v1/getUsers
GET    /api/v1/User/:id
POST   /api/v1/create_order
```

### HTTP Methods

| Method | Purpose | Idempotent | Request Body |
|--------|---------|------------|--------------|
| GET | Read resource(s) | Yes | No |
| POST | Create resource | No | Yes |
| PUT | Replace resource | Yes | Yes |
| PATCH | Partial update | Yes | Yes |
| DELETE | Remove resource | Yes | No |

### URL Patterns

```
# Collection operations
GET    /api/v1/users           # List all
POST   /api/v1/users           # Create one

# Single resource
GET    /api/v1/users/:id       # Get one
PUT    /api/v1/users/:id       # Replace one
PATCH  /api/v1/users/:id       # Update one
DELETE /api/v1/users/:id       # Delete one

# Nested resources
GET    /api/v1/users/:id/orders
POST   /api/v1/users/:id/orders

# Actions (when REST doesn't fit)
POST   /api/v1/users/:id/activate
POST   /api/v1/orders/:id/cancel
```

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "requestId": "req_abc123"
  }
}
```

### HTTP Status Codes

```
# Success
200 OK              - Successful GET, PUT, PATCH, DELETE
201 Created         - Successful POST creating resource
204 No Content      - Successful DELETE with no body

# Client Errors
400 Bad Request     - Invalid request syntax/body
401 Unauthorized    - Missing/invalid authentication
403 Forbidden       - Authenticated but not authorized
404 Not Found       - Resource doesn't exist
409 Conflict        - Resource state conflict
422 Unprocessable   - Validation errors

# Server Errors
500 Internal Error  - Unexpected server error
502 Bad Gateway     - Upstream service error
503 Unavailable     - Service temporarily down
```

### Error Handling Pattern

```typescript
// Error class hierarchy
class ApiError extends Error {
  constructor(
    public code: string,
    public message: string,
    public statusCode: number,
    public details?: unknown[]
  ) {
    super(message);
  }
}

class ValidationError extends ApiError {
  constructor(details: { field: string; message: string }[]) {
    super('VALIDATION_ERROR', 'Request validation failed', 422, details);
  }
}

class NotFoundError extends ApiError {
  constructor(resource: string, id: string) {
    super('NOT_FOUND', `${resource} with id ${id} not found`, 404);
  }
}

// Global error handler
function errorHandler(err: Error, req: Request, res: Response) {
  if (err instanceof ApiError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details,
        requestId: req.id
      }
    });
  }

  // Unexpected error - log and return generic message
  logger.error('Unhandled error', { error: err, requestId: req.id });
  return res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
      requestId: req.id
    }
  });
}
```

## API Versioning

### URL Path Versioning (Recommended)

```
GET /api/v1/users
GET /api/v2/users
```

### Implementation Pattern

```typescript
// Version-specific routers
const v1Router = Router();
const v2Router = Router();

v1Router.get('/users', getUsersV1);
v2Router.get('/users', getUsersV2);

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);
```

### Version Migration

```typescript
// Deprecation header
res.setHeader('Deprecation', 'true');
res.setHeader('Sunset', 'Sat, 01 Jan 2025 00:00:00 GMT');
res.setHeader('Link', '</api/v2/users>; rel="successor-version"');
```

## Pagination

### Cursor-Based (Recommended)

```json
// Request
GET /api/v1/users?limit=20&cursor=eyJpZCI6MTIzfQ

// Response
{
  "data": [...],
  "pagination": {
    "hasMore": true,
    "nextCursor": "eyJpZCI6MTQzfQ",
    "prevCursor": "eyJpZCI6MTAzfQ"
  }
}
```

### Offset-Based

```json
// Request
GET /api/v1/users?page=2&limit=20

// Response
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

## Request/Response Patterns

### Successful Responses

```typescript
// Single resource
res.status(200).json({ data: user });

// Collection
res.status(200).json({
  data: users,
  pagination: { ... }
});

// Created resource
res.status(201).json({ data: newUser });

// No content
res.status(204).send();
```

### Filtering and Sorting

```
# Filtering
GET /api/v1/users?status=active&role=admin

# Sorting
GET /api/v1/users?sort=createdAt:desc,name:asc

# Field selection
GET /api/v1/users?fields=id,name,email
```

## Quick Reference

### Endpoint Checklist

- [ ] Uses plural resource names
- [ ] Correct HTTP method for operation
- [ ] Returns appropriate status code
- [ ] Consistent error response format
- [ ] Includes request ID in errors
- [ ] Validates input before processing
- [ ] Documents in OpenAPI/Swagger
- [ ] Versioned URL path
- [ ] Pagination for list endpoints
- [ ] Rate limiting headers
