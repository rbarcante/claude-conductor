---
name: REST Conventions
category: API Design
tags: [api, rest, http, endpoints, resources]
activation:
  keywords: [api, rest, endpoint, route, url]
  file_patterns: ["**/routes/**", "**/api/**"]
---

# REST Conventions Pattern

## AI Quick Reference

**Purpose**: Design consistent, intuitive REST API endpoints following standard conventions.

**Key Rules**:
1. Use plural nouns for resources (`/users` not `/user`)
2. Use HTTP methods for operations (GET, POST, PUT, PATCH, DELETE)
3. Nest related resources (`/users/:id/orders`)
4. Use hyphens for multi-word resources (`/order-items`)
5. Version in URL path (`/api/v1/...`)

**Quick Patterns**:

```
# CRUD operations
GET    /api/v1/users           # List all
POST   /api/v1/users           # Create
GET    /api/v1/users/:id       # Get one
PUT    /api/v1/users/:id       # Replace
PATCH  /api/v1/users/:id       # Update
DELETE /api/v1/users/:id       # Delete

# Nested resources
GET    /api/v1/users/:id/orders
POST   /api/v1/users/:id/orders

# Actions (when REST doesn't fit)
POST   /api/v1/orders/:id/cancel
```

---

## Human Documentation

### When to Apply

- Designing new API endpoints
- Refactoring existing endpoints for consistency
- Reviewing API structure
- Planning API architecture

### Implementation Guide

#### 1. Resource Naming

**Good**:
- `/users` - plural noun
- `/order-items` - hyphen for compound words
- `/api/v1/products` - versioned path

**Avoid**:
- `/user` - singular
- `/getUsers` - verb in URL
- `/order_items` - underscores
- `/Users` - capitalized

#### 2. HTTP Method Selection

| Operation | Method | URL | Body |
|-----------|--------|-----|------|
| List | GET | /resources | No |
| Create | POST | /resources | Yes |
| Read | GET | /resources/:id | No |
| Replace | PUT | /resources/:id | Yes (full) |
| Update | PATCH | /resources/:id | Yes (partial) |
| Delete | DELETE | /resources/:id | No |

#### 3. Query Parameters

```
# Filtering
GET /users?status=active&role=admin

# Sorting
GET /users?sort=createdAt:desc

# Pagination
GET /users?page=2&limit=20

# Field selection
GET /users?fields=id,name,email

# Search
GET /users?q=john
```

#### 4. Nested vs Flat Resources

Use nested when relationship is strong:
```
GET /users/:id/orders      # User's orders
POST /users/:id/addresses  # Add address to user
```

Use flat when resource has independent identity:
```
GET /orders/:orderId       # Order by ID (not nested)
GET /addresses/:addressId  # Address by ID
```

### Anti-Patterns

- Verbs in URLs (`/createUser`, `/deleteOrder`)
- Inconsistent pluralization
- Deep nesting beyond 2 levels
- Using query params for required data

### Examples

See `SKILL.md` for comprehensive examples.
