---
name: typescript-best-practices
description: Use this skill when working with TypeScript code, type definitions, interfaces, generics, or async patterns.
version: 1.0.0
---

# TypeScript Best Practices

Guidance for writing type-safe, maintainable TypeScript code. Covers type safety fundamentals, async/await patterns, and null handling strategies.

## Core Principles

1. **Strict mode always**: Enable `strict: true` in tsconfig.json
2. **Explicit over implicit**: Prefer explicit types for public APIs
3. **Narrow types**: Use discriminated unions over loose object types
4. **Null safety**: Handle null/undefined explicitly with strict null checks
5. **Immutability**: Prefer `readonly` and `const` where possible

## Type Safety

### Prefer Interfaces for Object Shapes

```typescript
// Good - interfaces are more extensible
interface User {
  id: string;
  name: string;
  email: string;
}

// Use type for unions, intersections, mapped types
type UserRole = 'admin' | 'user' | 'guest';
type UserWithRole = User & { role: UserRole };
```

### Use Discriminated Unions for Variants

```typescript
// Good - exhaustive pattern matching
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function handleResult<T>(result: Result<T>) {
  if (result.success) {
    return result.data; // TypeScript knows data exists
  }
  throw result.error; // TypeScript knows error exists
}
```

### Avoid `any` - Use `unknown` Instead

```typescript
// Bad
function processData(data: any) {
  return data.value; // No type safety
}

// Good
function processData(data: unknown) {
  if (isValidData(data)) {
    return data.value; // Type narrowed via guard
  }
  throw new Error('Invalid data');
}

function isValidData(data: unknown): data is { value: string } {
  return typeof data === 'object' && data !== null && 'value' in data;
}
```

### Generic Constraints

```typescript
// Good - constrained generics
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Good - default type parameters
interface Repository<T extends { id: string } = { id: string }> {
  findById(id: string): Promise<T | null>;
  save(entity: T): Promise<T>;
}
```

## Async Patterns

### Always Await in Try-Catch

```typescript
// Good
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}
```

### Use Promise.all for Parallel Operations

```typescript
// Good - parallel execution
async function fetchUserData(userId: string) {
  const [user, posts, comments] = await Promise.all([
    fetchUser(userId),
    fetchUserPosts(userId),
    fetchUserComments(userId),
  ]);
  return { user, posts, comments };
}
```

### Type Async Return Values Explicitly

```typescript
// Good - explicit return type
async function createUser(data: CreateUserDTO): Promise<User> {
  const user = await db.users.create(data);
  return user;
}

// Good - handle errors with Result type
async function safeCreateUser(data: CreateUserDTO): Promise<Result<User>> {
  try {
    const user = await db.users.create(data);
    return { success: true, data: user };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}
```

## Null Handling

### Use Optional Chaining and Nullish Coalescing

```typescript
// Good
const userName = user?.profile?.name ?? 'Anonymous';
const config = options?.timeout ?? DEFAULT_TIMEOUT;

// Avoid
const userName = user && user.profile && user.profile.name || 'Anonymous';
```

### Non-Null Assertion Only When Certain

```typescript
// OK when you've verified externally
const element = document.getElementById('root')!;

// Better - explicit check
const element = document.getElementById('root');
if (!element) {
  throw new Error('Root element not found');
}
```

### Type Guards for Runtime Checks

```typescript
// Good - type guard function
function isDefined<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

// Usage
const values = [1, null, 2, undefined, 3];
const defined = values.filter(isDefined); // number[]
```

### Prefer `undefined` Over `null` for Optional

```typescript
// Good - consistent with optional properties
interface Options {
  timeout?: number; // undefined when not set
  retries?: number;
}

// Avoid mixing null and undefined
interface Options {
  timeout: number | null; // Inconsistent
  retries?: number;
}
```

## Utility Types

### Common Utility Type Patterns

```typescript
// Make all properties optional
type PartialUser = Partial<User>;

// Make all properties required
type RequiredUser = Required<User>;

// Pick specific properties
type UserCredentials = Pick<User, 'email' | 'password'>;

// Omit specific properties
type PublicUser = Omit<User, 'password'>;

// Make properties readonly
type ImmutableUser = Readonly<User>;

// Record for object maps
type UserCache = Record<string, User>;
```

### Extract and Exclude for Union Types

```typescript
type AllRoles = 'admin' | 'user' | 'guest' | 'superadmin';
type AdminRoles = Extract<AllRoles, 'admin' | 'superadmin'>; // 'admin' | 'superadmin'
type NonAdminRoles = Exclude<AllRoles, 'admin' | 'superadmin'>; // 'user' | 'guest'
```

## Quick Reference

### tsconfig.json Essentials

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true
  }
}
```

### Checklist

- [ ] `strict: true` enabled in tsconfig.json
- [ ] No `any` types without documented justification
- [ ] All async functions have error handling
- [ ] Public APIs have explicit return types
- [ ] Discriminated unions for variant types
- [ ] Type guards for runtime type checks
- [ ] `unknown` instead of `any` for unknown data
- [ ] Optional chaining for nullable access
- [ ] Nullish coalescing for default values
