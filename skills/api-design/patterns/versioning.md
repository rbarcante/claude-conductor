---
name: API Versioning
category: API Design
tags: [api, versioning, migration, deprecation]
activation:
  keywords: [version, versioning, deprecation, migration, v1, v2]
  file_patterns: ["**/api/**", "**/routes/**"]
---

# API Versioning Pattern

## AI Quick Reference

**Purpose**: Implement API versioning for safe evolution and backward compatibility.

**Key Rules**:
1. Version in URL path (`/api/v1/...`) - most explicit and recommended
2. Plan for versioning from day one
3. Maintain at least N-1 version
4. Use deprecation headers for sunset notice
5. Document breaking changes clearly

**Quick Patterns**:

```typescript
// URL path versioning (recommended)
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// Deprecation headers
res.setHeader('Deprecation', 'true');
res.setHeader('Sunset', 'Sat, 01 Jan 2025 00:00:00 GMT');
res.setHeader('Link', '</api/v2/users>; rel="successor-version"');
```

---

## Human Documentation

### When to Apply

- Setting up new API infrastructure
- Planning breaking changes
- Deprecating old API versions
- Migrating consumers to new versions

### Implementation Guide

#### 1. Versioning Strategies

**URL Path (Recommended)**:
```
GET /api/v1/users
GET /api/v2/users
```
- Most explicit and visible
- Easy to route and document
- Clear in logs and debugging

**Header-Based**:
```
GET /api/users
Accept: application/vnd.myapi.v1+json
```
- Cleaner URLs
- More complex to implement
- Harder to test/debug

**Query Parameter**:
```
GET /api/users?version=1
```
- Easy to implement
- Can be accidentally omitted
- Less RESTful

#### 2. Router Setup

```typescript
// v1/routes/users.ts
const v1Router = Router();
v1Router.get('/users', getUsersV1);
v1Router.post('/users', createUserV1);

// v2/routes/users.ts
const v2Router = Router();
v2Router.get('/users', getUsersV2);  // New response format
v2Router.post('/users', createUserV2);

// app.ts
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);
```

#### 3. Deprecation Process

**Phase 1: Announce** (6+ months before sunset)
```typescript
// Add deprecation headers
function deprecationMiddleware(req, res, next) {
  res.setHeader('Deprecation', 'true');
  res.setHeader('Sunset', 'Sat, 01 Jul 2025 00:00:00 GMT');
  res.setHeader('Link', '</api/v2>; rel="successor-version"');
  next();
}

v1Router.use(deprecationMiddleware);
```

**Phase 2: Warn** (3 months before)
- Log usage of deprecated endpoints
- Send notifications to known consumers
- Update documentation prominently

**Phase 3: Sunset**
- Return 410 Gone for removed endpoints
- Redirect or provide migration info

```typescript
function sunsetMiddleware(req, res) {
  res.status(410).json({
    error: {
      code: 'API_SUNSET',
      message: 'This API version is no longer available',
      migration: 'Please use /api/v2. See docs for migration guide.'
    }
  });
}
```

#### 4. Breaking vs Non-Breaking Changes

**Non-Breaking (no new version needed)**:
- Adding new endpoints
- Adding optional fields to responses
- Adding optional request parameters
- Bug fixes that don't change behavior

**Breaking (requires new version)**:
- Removing endpoints
- Removing/renaming fields
- Changing field types
- Changing authentication
- Changing error format

### Anti-Patterns

- No versioning from the start
- Too many active versions (keep max 2-3)
- Breaking changes without version bump
- Sudden deprecation without notice
- Incompatible version numbers

### Examples

See `SKILL.md` for comprehensive examples.
