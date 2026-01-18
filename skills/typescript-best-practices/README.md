# TypeScript Best Practices Skill

A Conductor skill providing guidance for writing type-safe, maintainable TypeScript code.

## Overview

This skill activates when working with TypeScript files and provides guidance on:

- **Type Safety**: Interfaces, generics, discriminated unions, type guards
- **Async Patterns**: Promise handling, error management, parallel execution
- **Null Handling**: Optional chaining, nullish coalescing, strict null checks

## Activation

The skill automatically activates when:

- Working with `.ts` or `.tsx` files
- Task description contains keywords: `typescript`, `type`, `interface`, `generic`, `async`
- Project tech stack includes TypeScript

## Patterns Provided

| Pattern | Description |
|---------|-------------|
| [type-safety](patterns/type-safety.md) | Type definitions, generics, discriminated unions |
| [async-patterns](patterns/async-patterns.md) | Async/await, Promise handling, error management |
| [null-handling](patterns/null-handling.md) | Null safety, optional chaining, type guards |

## Usage Examples

### Type-Safe API Response

```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  timestamp: string;
}

type ApiResult<T> =
  | { success: true; response: ApiResponse<T> }
  | { success: false; error: Error };

async function fetchApi<T>(url: string): Promise<ApiResult<T>> {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return {
      success: true,
      response: { data, status: response.status, timestamp: new Date().toISOString() }
    };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}
```

### Generic Repository Pattern

```typescript
interface Entity {
  id: string;
  createdAt: Date;
  updatedAt: Date;
}

interface Repository<T extends Entity> {
  findById(id: string): Promise<T | undefined>;
  findAll(): Promise<T[]>;
  create(data: Omit<T, 'id' | 'createdAt' | 'updatedAt'>): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}
```

## Configuration

Recommended `tsconfig.json` settings:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

## Related Skills

- **testing-strategies**: For TypeScript testing patterns
- **api-design**: For typed API development

## Changelog

### 1.0.0

- Initial release
- Type safety patterns
- Async/await patterns
- Null handling patterns
