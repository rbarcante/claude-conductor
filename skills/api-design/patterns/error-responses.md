---
name: Error Responses
category: API Design
tags: [api, errors, http, status-codes, validation]
activation:
  keywords: [error, exception, status, response, validation]
  file_patterns: ["**/errors/**", "**/middleware/**"]
---

# Error Responses Pattern

## AI Quick Reference

**Purpose**: Implement consistent, informative error responses across all API endpoints.

**Key Rules**:
1. Use standard HTTP status codes correctly
2. Return consistent JSON error format
3. Include error code, message, and details
4. Add request ID for debugging
5. Never expose internal errors to clients

**Quick Patterns**:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [{ "field": "email", "message": "Invalid format" }],
    "requestId": "req_abc123"
  }
}
```

```typescript
// Error class
class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number,
    public details?: unknown[]
  ) { super(message); }
}

// Usage
throw new ApiError('NOT_FOUND', 'User not found', 404);
```

---

## Human Documentation

### When to Apply

- Implementing error handling middleware
- Creating custom error classes
- Handling validation errors
- Designing error response format

### Implementation Guide

#### 1. HTTP Status Code Reference

**2xx Success**:
- `200` - OK (GET, PUT, PATCH success)
- `201` - Created (POST success)
- `204` - No Content (DELETE success)

**4xx Client Errors**:
- `400` - Bad Request (malformed syntax)
- `401` - Unauthorized (no/invalid auth)
- `403` - Forbidden (authenticated but not allowed)
- `404` - Not Found
- `409` - Conflict (state conflict)
- `422` - Unprocessable Entity (validation)
- `429` - Too Many Requests (rate limited)

**5xx Server Errors**:
- `500` - Internal Server Error
- `502` - Bad Gateway
- `503` - Service Unavailable

#### 2. Error Class Hierarchy

```typescript
// Base error
class ApiError extends Error {
  constructor(
    public code: string,
    public message: string,
    public statusCode: number,
    public details?: unknown[]
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Specific errors
class ValidationError extends ApiError {
  constructor(details: { field: string; message: string }[]) {
    super('VALIDATION_ERROR', 'Validation failed', 422, details);
  }
}

class NotFoundError extends ApiError {
  constructor(resource: string, id: string) {
    super('NOT_FOUND', `${resource} not found`, 404);
  }
}

class UnauthorizedError extends ApiError {
  constructor(message = 'Authentication required') {
    super('UNAUTHORIZED', message, 401);
  }
}

class ForbiddenError extends ApiError {
  constructor(message = 'Access denied') {
    super('FORBIDDEN', message, 403);
  }
}
```

#### 3. Error Handler Middleware

```typescript
function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  // Known API errors
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

  // Log unknown errors
  logger.error('Unhandled error', {
    error: err.message,
    stack: err.stack,
    requestId: req.id
  });

  // Generic response (don't expose internals)
  return res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
      requestId: req.id
    }
  });
}
```

### Anti-Patterns

- Exposing stack traces in production
- Inconsistent error formats
- Wrong status codes (200 for errors)
- Missing request IDs
- Leaking internal implementation details

### Examples

See `SKILL.md` for comprehensive examples.
