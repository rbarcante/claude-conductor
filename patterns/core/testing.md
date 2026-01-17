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
    - "**/*Test.java"
    - "**/*Tests.java"
    - "**/Test*.java"
    - "**/*Spec.java"
    - "**/*Test.kt"
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

```
test "should calculate total with discount":
    // Arrange - Set up test data and dependencies
    cart = new ShoppingCart()
    cart.addItem({ name: "Widget", price: 100 })
    discount = new PercentDiscount(10)

    // Act - Execute the code under test
    total = cart.calculateTotal(discount)

    // Assert - Verify the result
    assert total == 90
```

**Why this matters:**
- Easy to read and understand
- Clear separation of concerns
- Identifies what's being tested

#### Concept 3: Test Isolation

Tests should be independent and not affect each other:

```
// Bad: Tests share state
sharedUser = null

beforeAllTests():
    sharedUser = createUser()  // Shared across all tests

test "test1":
    sharedUser.name = "Changed"  // Modifies shared state

test "test2":
    assert sharedUser.name == "Original"  // FAILS due to test1!

// Good: Each test has its own data
test "test1":
    user = createUser()
    user.name = "Changed"
    assert user.name == "Changed"

test "test2":
    user = createUser()
    assert user.name == "Original"
```

### Implementation Examples

#### Example 1: Unit Test with Mocking

```
describe "OrderService":
    orderService = null
    mockPayment = null
    mockRepo = null

    beforeEachTest():
        // Create fresh mocks for each test
        mockPayment = createMock({
            charge: mockFunction(),
            refund: mockFunction()
        })
        mockRepo = createMock({
            save: mockFunction(),
            findById: mockFunction()
        })
        orderService = new OrderService(mockPayment, mockRepo)

    describe "placeOrder":
        test "should charge payment and save order on success":
            // Arrange
            order = { items: [{ id: "1", price: 100 }], total: 100 }
            mockPayment.charge.willReturn({ transactionId: "tx_123" })
            mockRepo.save.willReturn({ ...order, id: "order_1" })

            // Act
            result = orderService.placeOrder(order)

            // Assert
            assert mockPayment.charge.wasCalledWith(100)
            assert mockRepo.save.wasCalledWith(objectContaining({
                items: order.items,
                transactionId: "tx_123"
            }))
            assert result.id == "order_1"

        test "should not save order if payment fails":
            // Arrange
            order = { items: [{ id: "1", price: 100 }], total: 100 }
            mockPayment.charge.willThrow(Error("Card declined"))

            // Act & Assert
            assertThrows(
                function(): orderService.placeOrder(order),
                expectedError: "Card declined"
            )
            assert mockRepo.save.wasNotCalled()
```

#### Example 2: Integration Test with Test Database

```
describe "UserRepository Integration":
    db = null
    repo = null

    beforeAllTests():
        db = createTestDatabase()
        repo = new UserRepository(db)

    afterAllTests():
        cleanupTestDatabase(db)

    beforeEachTest():
        // Clean tables between tests
        db.execute("DELETE FROM users")

    test "should create and retrieve a user":
        // Arrange
        userData = { email: "test@example.com", name: "Test User" }

        // Act
        created = repo.create(userData)
        retrieved = repo.findById(created.id)

        // Assert
        assert retrieved.email == userData.email
        assert retrieved.name == userData.name
        assert retrieved.id == created.id

    test "should return null for non-existent user":
        result = repo.findById("non-existent-id")
        assert result is null
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
```
test "should call internal method correctly":
    service = new UserService()
    spy = spyOn(service, "_hashPassword")

    service.createUser({ password: "123" })

    assert spy.wasCalledWith("123", 10)  // Tests internal details!
```

**Why it's problematic:**
- Breaks when refactoring internal implementation
- Doesn't test actual behavior
- Creates brittle tests

**Better approach:**
```
test "should store hashed password, not plain text":
    service = new UserService()
    user = service.createUser({ password: "123" })

    assert user.password != "123"
    assert verifyPassword("123", user.password) == true
```

### Anti-Pattern 2: Test Interdependence

**What it looks like:**
```
createdUserId = null  // Shared state!

test "should create a user":
    user = api.createUser({ name: "Test" })
    createdUserId = user.id  // Sets shared state
    assert user.name == "Test"

test "should update the user":
    // DEPENDS on previous test running first!
    user = api.updateUser(createdUserId, { name: "Updated" })
    assert user.name == "Updated"
```

**Why it's problematic:**
- Tests fail when run in different order
- Hard to run single test in isolation
- Debugging is difficult

**Better approach:**
```
test "should create a user":
    user = api.createUser({ name: "Test" })
    assert user.name == "Test"
    api.deleteUser(user.id)  // Cleanup

test "should update a user":
    // Self-contained setup
    user = api.createUser({ name: "Test" })

    updated = api.updateUser(user.id, { name: "Updated" })

    assert updated.name == "Updated"
    api.deleteUser(user.id)  // Cleanup
```

### Anti-Pattern 3: Excessive Mocking

**What it looks like:**
```
test "should process order":
    mockUser = { id: "1", email: "test@test.com" }
    mockOrder = { id: "1", items: [] }
    mockPayment = { status: "success" }
    mockInventory = { available: true }
    mockShipping = { trackingId: "123" }
    mockEmail = { sent: true }
    // ... 10 more mocks

    // Test has become meaningless - what is even being tested?
```

**Why it's problematic:**
- Tests don't verify real behavior
- False confidence in code quality
- Tests pass but production breaks

**Better approach:**
```
// Unit test: mock external dependencies only
test "should validate order items":
    result = validateOrder({ items: [] })
    assert result.valid == false
    assert "Order must have at least one item" in result.errors

// Integration test: test component interactions with real(ish) dependencies
test "should process order end-to-end":
    // Use test database, mock only external services (payment, email)
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
