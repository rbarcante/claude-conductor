---
name: Integration Test Patterns
category: Testing
tags: [testing, integration, database, api]
activation:
  keywords: [integration, database, api, endpoint]
  file_patterns: ["**/integration/**", "**/*.integration.*"]
---

# Integration Test Patterns

## AI Quick Reference

**Purpose**: Test how components work together, including real external dependencies.

**Key Rules**:
1. Use real dependencies (database, file system) or realistic fakes
2. Isolate test data (separate DB, cleanup between tests)
3. Test the contract, not internal implementation
4. Handle async operations properly
5. Keep slower than unit tests but faster than E2E

**Quick Patterns**:

```typescript
describe('UserRepository Integration', () => {
  let db: Database;

  beforeAll(async () => { db = await createTestDb(); });
  afterAll(async () => { await db.close(); });
  beforeEach(async () => { await db.clear(); });

  it('should persist and retrieve user', async () => {
    const repo = new UserRepository(db);
    const saved = await repo.save({ name: 'John' });
    const found = await repo.findById(saved.id);
    expect(found).toEqual(saved);
  });
});
```

---

## Human Documentation

### When to Apply

- Testing database operations
- Testing API endpoints
- Testing service interactions
- Testing file system operations
- Verifying external service contracts

### Implementation Guide

#### 1. Database Integration

```typescript
describe('OrderRepository', () => {
  let db: TestDatabase;
  let repo: OrderRepository;

  beforeAll(async () => {
    db = await TestDatabase.create();
    await db.migrate();
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    await db.truncate(['orders', 'order_items']);
    repo = new OrderRepository(db.connection);
  });

  it('should create order with items', async () => {
    const order = await repo.create({
      userId: 'user-1',
      items: [
        { productId: 'prod-1', quantity: 2 },
        { productId: 'prod-2', quantity: 1 }
      ]
    });

    expect(order.id).toBeDefined();
    expect(order.items).toHaveLength(2);

    const found = await repo.findById(order.id);
    expect(found).toEqual(order);
  });
});
```

#### 2. API Integration

```typescript
describe('Users API', () => {
  let app: Application;
  let db: TestDatabase;

  beforeAll(async () => {
    db = await TestDatabase.create();
    app = createApp({ database: db.connection });
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    await db.truncate(['users']);
  });

  it('should create and retrieve user', async () => {
    // Create
    const createRes = await request(app)
      .post('/api/v1/users')
      .send({ name: 'John', email: 'john@example.com' });

    expect(createRes.status).toBe(201);
    const userId = createRes.body.data.id;

    // Retrieve
    const getRes = await request(app)
      .get(`/api/v1/users/${userId}`);

    expect(getRes.status).toBe(200);
    expect(getRes.body.data.name).toBe('John');
  });
});
```

#### 3. Test Isolation

- Use separate test database
- Clean up before each test (not after)
- Use transactions for faster cleanup
- Avoid test interdependencies

### Anti-Patterns

- Sharing mutable state between tests
- Not cleaning up test data
- Testing in production database
- Overly slow tests (>5s each)
- Flaky tests due to timing issues

### Examples

See `SKILL.md` for comprehensive examples.
