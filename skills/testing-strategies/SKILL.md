---
name: testing-strategies
description: Use this skill when writing tests, implementing TDD, or setting up test infrastructure.
version: 1.0.0
---

# Testing Strategies

Guidance for writing effective, maintainable tests. Covers unit testing patterns, integration testing, mocking strategies, and test organization.

## Core Principles

1. **Test behavior, not implementation**: Tests should verify what code does, not how
2. **Arrange-Act-Assert**: Structure every test with clear setup, action, and verification
3. **One assertion per concept**: Each test should verify one logical concept
4. **Independent tests**: Tests should not depend on each other or shared state
5. **Fast feedback**: Unit tests should run in milliseconds

## Test Structure

### Arrange-Act-Assert (AAA)

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // Arrange
      const userData = { name: 'John', email: 'john@example.com' };
      const mockRepo = { save: jest.fn().mockResolvedValue({ id: '1', ...userData }) };
      const service = new UserService(mockRepo);

      // Act
      const result = await service.createUser(userData);

      // Assert
      expect(result.id).toBe('1');
      expect(result.name).toBe('John');
      expect(mockRepo.save).toHaveBeenCalledWith(userData);
    });
  });
});
```

### Test Naming

```typescript
// Pattern: should [expected behavior] when [condition]
it('should return null when user not found', () => {});
it('should throw ValidationError when email is invalid', () => {});
it('should retry 3 times when connection fails', () => {});

// Or: [condition] => [expected behavior]
it('invalid email => throws ValidationError', () => {});
it('user not found => returns null', () => {});
```

### Test Organization

```
src/
  services/
    user.ts
    user.test.ts          # Co-located unit tests
tests/
  integration/
    user.integration.ts   # Integration tests
  e2e/
    user-flow.e2e.ts      # End-to-end tests
  fixtures/
    users.ts              # Shared test data
  helpers/
    test-db.ts            # Test utilities
```

## Unit Testing

### Pure Functions

```typescript
// Function to test
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// Tests
describe('calculateTotal', () => {
  it('should return 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('should calculate total for single item', () => {
    const items = [{ price: 10, quantity: 2 }];
    expect(calculateTotal(items)).toBe(20);
  });

  it('should calculate total for multiple items', () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 3 }
    ];
    expect(calculateTotal(items)).toBe(35);
  });
});
```

### Classes with Dependencies

```typescript
// Class to test
class OrderService {
  constructor(
    private orderRepo: OrderRepository,
    private paymentGateway: PaymentGateway
  ) {}

  async placeOrder(order: Order): Promise<OrderResult> {
    const savedOrder = await this.orderRepo.save(order);
    const payment = await this.paymentGateway.charge(order.total);
    return { order: savedOrder, payment };
  }
}

// Test with mocks
describe('OrderService', () => {
  let service: OrderService;
  let mockOrderRepo: jest.Mocked<OrderRepository>;
  let mockPaymentGateway: jest.Mocked<PaymentGateway>;

  beforeEach(() => {
    mockOrderRepo = { save: jest.fn() };
    mockPaymentGateway = { charge: jest.fn() };
    service = new OrderService(mockOrderRepo, mockPaymentGateway);
  });

  it('should save order and charge payment', async () => {
    // Arrange
    const order = { id: '1', total: 100 };
    mockOrderRepo.save.mockResolvedValue(order);
    mockPaymentGateway.charge.mockResolvedValue({ success: true });

    // Act
    const result = await service.placeOrder(order);

    // Assert
    expect(mockOrderRepo.save).toHaveBeenCalledWith(order);
    expect(mockPaymentGateway.charge).toHaveBeenCalledWith(100);
    expect(result.order).toEqual(order);
  });
});
```

## Mocking Strategies

### When to Mock

**Mock**:
- External services (APIs, databases, file system)
- Non-deterministic operations (time, random)
- Slow operations (network, disk)
- Operations with side effects

**Don't Mock**:
- Pure functions
- Simple data transformations
- The code under test itself

### Mock Types

```typescript
// Stub - returns canned response
const userRepo = { findById: jest.fn().mockResolvedValue(mockUser) };

// Spy - tracks calls while using real implementation
const spy = jest.spyOn(console, 'log');
// ... run code
expect(spy).toHaveBeenCalledWith('message');

// Fake - simplified working implementation
class FakeUserRepo implements UserRepository {
  private users: Map<string, User> = new Map();

  async save(user: User) {
    this.users.set(user.id, user);
    return user;
  }

  async findById(id: string) {
    return this.users.get(id);
  }
}
```

### Mocking Patterns

```typescript
// Mock module
jest.mock('./database', () => ({
  query: jest.fn()
}));

// Mock specific method
jest.spyOn(Date, 'now').mockReturnValue(1234567890);

// Mock implementation
mockFn.mockImplementation((x) => x * 2);

// Mock once (for specific test)
mockFn.mockResolvedValueOnce(firstResult);
mockFn.mockResolvedValueOnce(secondResult);

// Reset mocks between tests
beforeEach(() => {
  jest.clearAllMocks();
});
```

## Integration Testing

### Database Integration

```typescript
describe('UserRepository', () => {
  let db: Database;
  let repo: UserRepository;

  beforeAll(async () => {
    db = await createTestDatabase();
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    await db.clear();
    repo = new UserRepository(db);
  });

  it('should persist and retrieve user', async () => {
    // Arrange
    const user = { name: 'John', email: 'john@example.com' };

    // Act
    const saved = await repo.create(user);
    const found = await repo.findById(saved.id);

    // Assert
    expect(found).toEqual(saved);
  });
});
```

### API Integration

```typescript
describe('POST /api/users', () => {
  let app: Express;

  beforeAll(() => {
    app = createApp();
  });

  it('should create user and return 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'john@example.com' });

    expect(response.status).toBe(201);
    expect(response.body.data).toHaveProperty('id');
    expect(response.body.data.name).toBe('John');
  });

  it('should return 422 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'invalid' });

    expect(response.status).toBe(422);
    expect(response.body.error.code).toBe('VALIDATION_ERROR');
  });
});
```

## Test Coverage

### Coverage Targets

| Metric | Target | Critical Path |
|--------|--------|---------------|
| Line | 80% | 95%+ |
| Branch | 75% | 90%+ |
| Function | 85% | 95%+ |

### Meaningful Coverage

```typescript
// Don't write tests just for coverage
// Bad - tests implementation, not behavior
it('should call validateEmail', () => {
  service.createUser({ email: 'test@example.com' });
  expect(validateEmail).toHaveBeenCalled();
});

// Good - tests actual behavior
it('should reject invalid email format', () => {
  expect(() => service.createUser({ email: 'invalid' }))
    .toThrow(ValidationError);
});
```

## Quick Reference

### Test Checklist

- [ ] Test names describe expected behavior
- [ ] Each test follows AAA pattern
- [ ] Tests are independent (no shared state)
- [ ] Mocks only external dependencies
- [ ] Edge cases covered (null, empty, error)
- [ ] Error scenarios tested
- [ ] Tests run fast (<100ms per unit test)
- [ ] No flaky tests (deterministic)

### Common Assertions

```typescript
// Equality
expect(value).toBe(expected);           // Strict equality
expect(value).toEqual(expected);        // Deep equality
expect(value).toBeNull();
expect(value).toBeDefined();

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeLessThanOrEqual(10);
expect(value).toBeCloseTo(0.3, 5);      // Floating point

// Strings
expect(str).toMatch(/pattern/);
expect(str).toContain('substring');

// Arrays
expect(array).toContain(item);
expect(array).toHaveLength(3);

// Objects
expect(obj).toHaveProperty('key');
expect(obj).toMatchObject({ key: 'value' });

// Exceptions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow(ErrorType);
expect(() => fn()).toThrow('message');

// Async
await expect(promise).resolves.toBe(value);
await expect(promise).rejects.toThrow();
```
