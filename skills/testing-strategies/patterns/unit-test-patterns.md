---
name: Unit Test Patterns
category: Testing
tags: [testing, unit-test, tdd, assertions]
activation:
  keywords: [unit, test, assert, expect]
  file_patterns: ["**/*.test.*", "**/*.spec.*"]
---

# Unit Test Patterns

## AI Quick Reference

**Purpose**: Write focused, maintainable unit tests that verify behavior, not implementation.

**Key Rules**:
1. Follow AAA pattern (Arrange-Act-Assert)
2. One logical concept per test
3. Descriptive test names (`should X when Y`)
4. Test behavior, not implementation details
5. Keep tests independent (no shared mutable state)

**Quick Patterns**:

```typescript
describe('ClassName/FunctionName', () => {
  describe('methodName', () => {
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      const input = createTestData();

      // Act
      const result = functionUnderTest(input);

      // Assert
      expect(result).toBe(expected);
    });
  });
});
```

---

## Human Documentation

### When to Apply

- Testing individual functions or methods
- Testing class behavior in isolation
- Verifying business logic
- Testing edge cases and error handling

### Implementation Guide

#### 1. Test Structure

**Describe blocks for organization**:
```typescript
describe('Calculator', () => {
  describe('add', () => {
    it('should add two positive numbers', () => {});
    it('should handle negative numbers', () => {});
    it('should return 0 when both inputs are 0', () => {});
  });

  describe('divide', () => {
    it('should divide two numbers', () => {});
    it('should throw when dividing by zero', () => {});
  });
});
```

#### 2. Test Naming Conventions

```typescript
// Pattern 1: should [behavior] when [condition]
it('should return empty array when input is empty', () => {});
it('should throw ValidationError when email is invalid', () => {});

// Pattern 2: [condition] => [behavior]
it('empty input => returns empty array', () => {});
it('invalid email => throws ValidationError', () => {});
```

#### 3. Edge Cases to Cover

- Empty inputs (null, undefined, empty string, empty array)
- Boundary values (0, -1, MAX_INT)
- Error conditions
- Single item vs multiple items
- Invalid types

#### 4. Test Data

```typescript
// Use factory functions for test data
function createUser(overrides = {}): User {
  return {
    id: '1',
    name: 'Test User',
    email: 'test@example.com',
    ...overrides
  };
}

// Usage
it('should update user name', () => {
  const user = createUser({ name: 'Original' });
  // ...
});
```

### Anti-Patterns

- Testing implementation details
- Multiple assertions testing different concepts
- Tests that depend on other tests
- Hardcoded magic values without explanation
- Testing getters/setters directly

### Examples

See `SKILL.md` for comprehensive examples.
