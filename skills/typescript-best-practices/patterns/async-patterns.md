---
name: Async Patterns
category: TypeScript
tags: [typescript, async, await, promise, error-handling]
activation:
  keywords: [async, await, promise, fetch, api]
  file_patterns: ["**/*.ts", "**/*.tsx"]
---

# Async Patterns

## AI Quick Reference

**Purpose**: Write correct, efficient, and error-safe asynchronous TypeScript code.

**Key Rules**:
1. Always use try-catch with async/await
2. Type async return values explicitly
3. Use Promise.all for parallel operations
4. Return Result types for recoverable errors
5. Avoid floating promises (always await or handle)

**Quick Patterns**:

```typescript
// Explicit return type
async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}

// Parallel execution
const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()]);

// Result type for errors
type Result<T> = { ok: true; data: T } | { ok: false; error: Error };

async function safeFetch<T>(url: string): Promise<Result<T>> {
  try {
    const res = await fetch(url);
    return { ok: true, data: await res.json() };
  } catch (e) {
    return { ok: false, error: e as Error };
  }
}
```

---

## Human Documentation

### When to Apply

- API calls and network requests
- Database operations
- File system operations
- Any I/O-bound operations
- Operations that may fail

### Implementation Guide

#### 1. Error Handling

Always wrap async operations in try-catch:

```typescript
async function processOrder(orderId: string): Promise<Order> {
  try {
    const order = await fetchOrder(orderId);
    await validateOrder(order);
    await processPayment(order);
    return order;
  } catch (error) {
    logger.error('Order processing failed', { orderId, error });
    throw new OrderProcessingError(orderId, error as Error);
  }
}
```

#### 2. Parallel vs Sequential

```typescript
// Sequential - use when order matters or resources are limited
for (const item of items) {
  await processItem(item);
}

// Parallel - use for independent operations
await Promise.all(items.map(item => processItem(item)));

// Controlled parallelism - limit concurrent operations
async function processWithLimit<T, R>(
  items: T[],
  fn: (item: T) => Promise<R>,
  limit: number
): Promise<R[]> {
  const results: R[] = [];
  for (let i = 0; i < items.length; i += limit) {
    const batch = items.slice(i, i + limit);
    const batchResults = await Promise.all(batch.map(fn));
    results.push(...batchResults);
  }
  return results;
}
```

#### 3. Cancellation

Use AbortController for cancellable operations:

```typescript
async function fetchWithTimeout<T>(
  url: string,
  timeoutMs: number
): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, { signal: controller.signal });
    return response.json();
  } finally {
    clearTimeout(timeoutId);
  }
}
```

### Anti-Patterns

- Floating promises (not awaiting or handling)
- Sequential awaits for independent operations
- Missing error handling
- Not typing Promise return values
- Using `.then()` chains instead of async/await

### Examples

See `SKILL.md` for comprehensive examples.
