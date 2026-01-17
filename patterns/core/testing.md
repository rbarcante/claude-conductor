---
name: "Testing"
category: "Quality"
tags:
  - testing
  - unit-tests
  - integration
  - mocking
  - coverage
activation:
  keywords:
    - test
    - testing
    - unit
    - integration
    - mock
    - assert
    - coverage
    - spec
    - tdd
  file_patterns:
    - "**/*.test.{js,ts}"
    - "**/*.spec.{js,ts}"
    - "**/test_*.py"
    - "**/*_test.{go,rs}"
version: "1.0"
last_updated: "2026-01-19"
---

# Testing

> Write effective tests with clear structure, proper isolation, and meaningful assertions.

---

## AI Quick Reference

### When to Apply
- Writing new features (TDD: test first)
- Fixing bugs (write test to reproduce, then fix)
- Refactoring code (tests as safety net)
- Adding test coverage to existing code

### Core Principles
1. **Test Behavior, Not Implementation**: Focus on what, not how
2. **Arrange-Act-Assert**: Clear test structure
3. **One Assertion Per Concept**: Each test verifies one thing
4. **Isolated Tests**: Tests don't depend on each other
5. **Fast Feedback**: Unit tests should run in milliseconds

### Quick Implementation Checklist
- [ ] Follow AAA pattern (Arrange, Act, Assert)
- [ ] Name tests descriptively (should_returnError_when_inputInvalid)
- [ ] Mock external dependencies
- [ ] Test edge cases and error paths
- [ ] Aim for >80% coverage on business logic
- [ ] Keep tests fast (<100ms per unit test)

### Code Pattern (Pseudocode)
```
// Unit test structure
describe('UserService') {
    describe('createUser') {
        it('should create user with valid input', async () => {
            // Arrange
            const mockRepo = createMock(UserRepository)
            mockRepo.save.returns({ id: '123', ...validUser })
            const service = new UserService(mockRepo)

            // Act
            const result = await service.createUser(validUser)

            // Assert
            expect(result.id).toBe('123')
            expect(mockRepo.save).toHaveBeenCalledWith(validUser)
        })

        it('should throw ValidationError when email invalid', async () => {
            // Arrange
            const service = new UserService(mockRepo)

            // Act & Assert
            await expect(service.createUser({ email: 'invalid' }))
                .rejects.toThrow(ValidationError)
        })
    }
}
```

### Key Decisions
| Decision Point | Recommended Choice | Rationale |
|----------------|-------------------|-----------|
| Test framework | Jest, Vitest, pytest | Community support, features |
| Mocking | Built-in or minimal library | Less complexity |
| Coverage target | 80% for business logic | Balance cost/benefit |
| Test location | Co-located with code | Easy to find and maintain |

---

## Human Documentation

### Overview

Testing is essential for building reliable software. Good tests:
- Catch bugs before users do
- Enable confident refactoring
- Document expected behavior
- Provide design feedback (hard to test = poor design)

This pattern covers unit and integration testing strategies, test structure, mocking, and coverage approaches.

### Detailed Explanation

#### Concept 1: Test Pyramid

The test pyramid guides how many tests of each type to write:

```
         /\
        /  \  E2E Tests (few, slow, expensive)
       /----\
      /      \  Integration Tests (some, medium speed)
     /--------\
    /          \  Unit Tests (many, fast, cheap)
   /____________\
```

| Type | Scope | Speed | When to Use |
|------|-------|-------|-------------|
| **Unit** | Single function/class | <10ms | Business logic, utilities |
| **Integration** | Multiple components | 100ms-1s | APIs, database queries |
| **E2E** | Full application | 10s+ | Critical user paths |

#### Concept 2: AAA Pattern (Arrange-Act-Assert)

Every test should have three distinct sections:

```typescript
it('should calculate total with discount', () => {
    // Arrange - Set up test data and dependencies
    const cart = new ShoppingCart();
    cart.addItem({ name: 'Widget', price: 100 });
    const discount = new PercentDiscount(10);

    // Act - Execute the code under test
    const total = cart.calculateTotal(discount);

    // Assert - Verify the result
    expect(total).toBe(90);
});
```

**Why this matters:**
- Easy to read and understand
- Clear separation of concerns
- Identifies what's being tested

#### Concept 3: Test Isolation

Tests should be independent and not affect each other:

```typescript
// Bad: Tests share state
let user;

beforeAll(() => {
    user = createUser(); // Shared across all tests
});

it('test1', () => {
    user.name = 'Changed'; // Modifies shared state
});

it('test2', () => {
    expect(user.name).toBe('Original'); // Fails due to test1
});

// Good: Each test has its own data
it('test1', () => {
    const user = createUser();
    user.name = 'Changed';
    expect(user.name).toBe('Changed');
});

it('test2', () => {
    const user = createUser();
    expect(user.name).toBe('Original');
});
```

### Implementation Examples

#### Example 1: Unit Test with Mocking

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { OrderService } from './order-service';
import { PaymentGateway } from './payment-gateway';
import { OrderRepository } from './order-repository';

describe('OrderService', () => {
    let orderService: OrderService;
    let mockPayment: PaymentGateway;
    let mockRepo: OrderRepository;

    beforeEach(() => {
        // Create fresh mocks for each test
        mockPayment = {
            charge: vi.fn(),
            refund: vi.fn(),
        };
        mockRepo = {
            save: vi.fn(),
            findById: vi.fn(),
        };
        orderService = new OrderService(mockPayment, mockRepo);
    });

    describe('placeOrder', () => {
        it('should charge payment and save order on success', async () => {
            // Arrange
            const order = { items: [{ id: '1', price: 100 }], total: 100 };
            mockPayment.charge.mockResolvedValue({ transactionId: 'tx_123' });
            mockRepo.save.mockResolvedValue({ ...order, id: 'order_1' });

            // Act
            const result = await orderService.placeOrder(order);

            // Assert
            expect(mockPayment.charge).toHaveBeenCalledWith(100);
            expect(mockRepo.save).toHaveBeenCalledWith(
                expect.objectContaining({
                    items: order.items,
                    transactionId: 'tx_123',
                })
            );
            expect(result.id).toBe('order_1');
        });

        it('should not save order if payment fails', async () => {
            // Arrange
            const order = { items: [{ id: '1', price: 100 }], total: 100 };
            mockPayment.charge.mockRejectedValue(new Error('Card declined'));

            // Act & Assert
            await expect(orderService.placeOrder(order))
                .rejects.toThrow('Card declined');
            expect(mockRepo.save).not.toHaveBeenCalled();
        });
    });
});
```

#### Example 2: Integration Test with Test Database

```typescript
import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest';
import { createTestDatabase, cleanupTestDatabase } from './test-utils';
import { UserRepository } from './user-repository';

describe('UserRepository Integration', () => {
    let db;
    let repo: UserRepository;

    beforeAll(async () => {
        db = await createTestDatabase();
        repo = new UserRepository(db);
    });

    afterAll(async () => {
        await cleanupTestDatabase(db);
    });

    beforeEach(async () => {
        // Clean tables between tests
        await db.query('DELETE FROM users');
    });

    it('should create and retrieve a user', async () => {
        // Arrange
        const userData = { email: 'test@example.com', name: 'Test User' };

        // Act
        const created = await repo.create(userData);
        const retrieved = await repo.findById(created.id);

        // Assert
        expect(retrieved).toMatchObject(userData);
        expect(retrieved.id).toBe(created.id);
    });

    it('should return null for non-existent user', async () => {
        const result = await repo.findById('non-existent-id');
        expect(result).toBeNull();
    });
});
```

### Best Practices

1. **Descriptive Test Names**: Use `should_expectedBehavior_when_condition` or similar patterns that read like sentences.

2. **Test Edge Cases**: Empty arrays, null values, boundary conditions, error scenarios.

3. **Don't Test Implementation Details**: If you change how something works but not what it does, tests shouldn't break.

4. **Use Test Fixtures/Factories**: Create helper functions for common test data setup.

5. **Run Tests in CI**: Automated testing on every commit catches regressions early.

### Trade-offs and Considerations

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| TDD (Test First) | Better design, high coverage | Slower initial development | New features, refactoring |
| TAD (Test After) | Faster initial development | May miss edge cases | Prototypes, spikes |
| BDD (Behavior-Driven) | Stakeholder-readable | More verbose | User-facing features |
| Property-Based | Finds edge cases automatically | Harder to write | Algorithms, data processing |

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Testing Implementation Details

**What it looks like:**
```typescript
it('should call internal method correctly', () => {
    const service = new UserService();
    const spy = vi.spyOn(service, '_hashPassword');

    service.createUser({ password: '123' });

    expect(spy).toHaveBeenCalledWith('123', 10); // Tests internal details
});
```

**Why it's problematic:**
- Breaks when refactoring internal implementation
- Doesn't test actual behavior
- Creates brittle tests

**Better approach:**
```typescript
it('should store hashed password, not plain text', async () => {
    const service = new UserService();
    const user = await service.createUser({ password: '123' });

    expect(user.password).not.toBe('123');
    expect(await verifyPassword('123', user.password)).toBe(true);
});
```

### Anti-Pattern 2: Test Interdependence

**What it looks like:**
```typescript
let createdUserId;

it('should create a user', async () => {
    const user = await api.createUser({ name: 'Test' });
    createdUserId = user.id; // Shared state!
    expect(user.name).toBe('Test');
});

it('should update the user', async () => {
    // Depends on previous test!
    const user = await api.updateUser(createdUserId, { name: 'Updated' });
    expect(user.name).toBe('Updated');
});
```

**Why it's problematic:**
- Tests fail when run in different order
- Hard to run single test in isolation
- Debugging is difficult

**Better approach:**
```typescript
it('should create a user', async () => {
    const user = await api.createUser({ name: 'Test' });
    expect(user.name).toBe('Test');
    await api.deleteUser(user.id); // Cleanup
});

it('should update a user', async () => {
    // Self-contained setup
    const user = await api.createUser({ name: 'Test' });

    const updated = await api.updateUser(user.id, { name: 'Updated' });

    expect(updated.name).toBe('Updated');
    await api.deleteUser(user.id); // Cleanup
});
```

### Anti-Pattern 3: Excessive Mocking

**What it looks like:**
```typescript
it('should process order', async () => {
    const mockUser = { id: '1', email: 'test@test.com' };
    const mockOrder = { id: '1', items: [] };
    const mockPayment = { status: 'success' };
    const mockInventory = { available: true };
    const mockShipping = { trackingId: '123' };
    const mockEmail = { sent: true };
    // ... 10 more mocks

    // Test has become meaningless - what is even being tested?
});
```

**Why it's problematic:**
- Tests don't verify real behavior
- False confidence in code quality
- Tests pass but production breaks

**Better approach:**
```typescript
// Unit test: mock external dependencies only
it('should validate order items', () => {
    const result = validateOrder({ items: [] });
    expect(result.valid).toBe(false);
    expect(result.errors).toContain('Order must have at least one item');
});

// Integration test: test component interactions with real(ish) dependencies
it('should process order end-to-end', async () => {
    // Use test database, mock only external services (payment, email)
});
```

---

## Related Patterns

- [Error Handling](./error-handling.md) - Test error paths and error messages
- [Validation](./validation.md) - Test validation logic with edge cases

---

## References

- [Testing Library](https://testing-library.com/) - User-centric testing
- [Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html) - Martin Fowler's guide
- [TDD by Example](https://www.oreilly.com/library/view/test-driven-development/0321146530/) - Kent Beck's classic
