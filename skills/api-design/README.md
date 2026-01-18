# API Design Skill

A Conductor skill providing guidance for designing and implementing RESTful APIs.

## Overview

This skill activates when working with API-related code and provides guidance on:

- **REST Conventions**: URL naming, HTTP methods, resource design
- **Error Responses**: Standardized error format, status codes
- **Versioning**: URL path versioning, deprecation, migration

## Activation

The skill automatically activates when:

- Working with files in `routes/`, `controllers/`, `api/`, or `endpoints/` directories
- Task description contains keywords: `api`, `endpoint`, `rest`, `route`, `controller`
- Project tech stack includes backend frameworks (Express, FastAPI, etc.)

## Patterns Provided

| Pattern | Description |
|---------|-------------|
| [rest-conventions](patterns/rest-conventions.md) | URL naming, HTTP methods, resource design |
| [error-responses](patterns/error-responses.md) | Error format, status codes, error classes |
| [versioning](patterns/versioning.md) | URL versioning, deprecation, migration |

## Usage Examples

### RESTful User Endpoint

```typescript
import { Router } from 'express';
import { validateBody } from '../middleware/validation';
import { UserService } from '../services/user';
import { NotFoundError, ValidationError } from '../errors';

const router = Router();
const userService = new UserService();

// GET /api/v1/users
router.get('/', async (req, res) => {
  const { page = 1, limit = 20 } = req.query;
  const result = await userService.findAll({ page, limit });
  res.json({
    data: result.users,
    pagination: {
      page: result.page,
      limit: result.limit,
      total: result.total,
      totalPages: result.totalPages
    }
  });
});

// GET /api/v1/users/:id
router.get('/:id', async (req, res) => {
  const user = await userService.findById(req.params.id);
  if (!user) {
    throw new NotFoundError('User', req.params.id);
  }
  res.json({ data: user });
});

// POST /api/v1/users
router.post('/', validateBody(createUserSchema), async (req, res) => {
  const user = await userService.create(req.body);
  res.status(201).json({ data: user });
});

// PATCH /api/v1/users/:id
router.patch('/:id', validateBody(updateUserSchema), async (req, res) => {
  const user = await userService.update(req.params.id, req.body);
  if (!user) {
    throw new NotFoundError('User', req.params.id);
  }
  res.json({ data: user });
});

// DELETE /api/v1/users/:id
router.delete('/:id', async (req, res) => {
  await userService.delete(req.params.id);
  res.status(204).send();
});

export default router;
```

### Error Handler

```typescript
import { Request, Response, NextFunction } from 'express';
import { ApiError } from '../errors';
import { logger } from '../utils/logger';

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
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

## Best Practices

1. **Version from the start** - Always include version in URL path
2. **Consistent error format** - Same structure for all errors
3. **Validate early** - Use middleware for request validation
4. **Document everything** - OpenAPI/Swagger for all endpoints
5. **Include request IDs** - Trace requests through logs

## Related Skills

- **typescript-best-practices**: For typed API development
- **testing-strategies**: For API testing patterns

## Changelog

### 1.0.0

- Initial release
- REST conventions patterns
- Error response patterns
- Versioning patterns
