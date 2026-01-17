---
name: Type Safety
category: TypeScript
tags: [typescript, types, interfaces, generics, discriminated-unions]
activation:
  keywords: [type, interface, generic, union, typescript]
  file_patterns: ["**/*.ts", "**/*.tsx"]
---

# Type Safety Pattern

## AI Quick Reference

**Purpose**: Ensure compile-time type safety and runtime type correctness in TypeScript code.

**Key Rules**:
1. Use `interface` for object shapes, `type` for unions/intersections
2. Prefer discriminated unions over optional properties for variants
3. Use `unknown` instead of `any` for unknown data
4. Add explicit return types to public functions
5. Use type guards for runtime narrowing

**Quick Patterns**:

```typescript
// Discriminated union
type Result<T> = { ok: true; value: T } | { ok: false; error: Error };

// Type guard
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null && 'id' in obj;
}

// Generic constraint
function first<T extends { length: number }>(arr: T): T[0] | undefined {
  return arr[0];
}
```

---

## Human Documentation

### When to Apply

- Defining data structures and API contracts
- Working with external data (API responses, user input)
- Creating reusable generic components
- Handling multiple possible states/outcomes

### Implementation Guide

#### 1. Interface vs Type

Use **interfaces** for:
- Object shapes that may be extended
- Public API contracts
- Class implementations

Use **types** for:
- Union types (`type Status = 'pending' | 'done'`)
- Intersection types (`type Admin = User & AdminPermissions`)
- Mapped/conditional types

#### 2. Discriminated Unions

Instead of optional properties:

```typescript
// Avoid
interface ApiResponse {
  data?: User;
  error?: string;
  loading?: boolean;
}

// Prefer
type ApiResponse =
  | { status: 'loading' }
  | { status: 'success'; data: User }
  | { status: 'error'; error: string };
```

#### 3. Type Guards

Create reusable type guards for runtime checks:

```typescript
function isNonNull<T>(value: T | null | undefined): value is T {
  return value != null;
}

function hasProperty<K extends string>(obj: unknown, key: K): obj is Record<K, unknown> {
  return typeof obj === 'object' && obj !== null && key in obj;
}
```

### Anti-Patterns

- Using `any` without justification
- Casting with `as` to bypass type errors
- Empty interfaces or overly permissive types
- Ignoring TypeScript errors with `@ts-ignore`

### Examples

See `SKILL.md` for comprehensive examples.
