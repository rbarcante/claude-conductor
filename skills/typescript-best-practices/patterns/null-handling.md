---
name: Null Handling
category: TypeScript
tags: [typescript, null, undefined, optional, type-guard]
activation:
  keywords: [null, undefined, optional, nullable, nullish]
  file_patterns: ["**/*.ts", "**/*.tsx"]
---

# Null Handling Pattern

## AI Quick Reference

**Purpose**: Safely handle null and undefined values with TypeScript's strict null checks.

**Key Rules**:
1. Enable `strictNullChecks` in tsconfig.json
2. Use optional chaining (`?.`) for nullable access
3. Use nullish coalescing (`??`) for default values
4. Prefer `undefined` over `null` for consistency
5. Use type guards for runtime narrowing

**Quick Patterns**:

```typescript
// Optional chaining
const name = user?.profile?.name;

// Nullish coalescing
const timeout = config.timeout ?? DEFAULT_TIMEOUT;

// Type guard
function isDefined<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

// Filter nulls
const defined = items.filter(isDefined);

// Assertion with error
function assertDefined<T>(value: T | null | undefined, msg?: string): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(msg ?? 'Value is null or undefined');
  }
}
```

---

## Human Documentation

### When to Apply

- Accessing nested optional properties
- Providing default values
- Working with external data (APIs, databases)
- Optional function parameters
- DOM element access

### Implementation Guide

#### 1. Optional Chaining

```typescript
// Instead of
const city = user && user.address && user.address.city;

// Use
const city = user?.address?.city;

// With method calls
const result = obj?.method?.();

// With array access
const first = arr?.[0];
```

#### 2. Nullish Coalescing

```typescript
// Instead of (which treats 0 and '' as falsy)
const count = config.count || 10;

// Use (only replaces null/undefined)
const count = config.count ?? 10;

// Combined with optional chaining
const name = user?.name ?? 'Anonymous';
```

#### 3. Type Guards

```typescript
// Simple null check
function isNotNull<T>(value: T | null): value is T {
  return value !== null;
}

// Combined null/undefined check
function isDefined<T>(value: T | null | undefined): value is T {
  return value != null; // Checks both null and undefined
}

// Array filter usage
const validUsers = users.filter(isDefined);
```

#### 4. Assertion Functions

```typescript
function assertDefined<T>(
  value: T | null | undefined,
  message?: string
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message ?? 'Unexpected null or undefined');
  }
}

// Usage
function processUser(user: User | null) {
  assertDefined(user, 'User is required');
  // TypeScript knows user is User here
  console.log(user.name);
}
```

### Anti-Patterns

- Using `!` (non-null assertion) without verification
- Mixing `null` and `undefined` inconsistently
- Using `||` when `??` is more appropriate
- Not handling null cases in function signatures

### Configuration

Enable in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": true
  }
}
```

### Examples

See `SKILL.md` for comprehensive examples.
