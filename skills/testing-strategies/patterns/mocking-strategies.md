---
name: Mocking Strategies
category: Testing
tags: [testing, mocking, stubs, spies, fakes]
activation:
  keywords: [mock, stub, spy, fake, jest]
  file_patterns: ["**/*.test.*", "**/*.spec.*"]
---

# Mocking Strategies Pattern

## AI Quick Reference

**Purpose**: Isolate code under test by replacing dependencies with controlled substitutes.

**Key Rules**:
1. Only mock external dependencies and I/O
2. Don't mock the code under test
3. Prefer fakes over mocks for complex behavior
4. Reset mocks between tests
5. Verify interactions when behavior matters

**Quick Patterns**:

```typescript
// Stub - returns canned response
const mockRepo = { findById: jest.fn().mockResolvedValue(mockUser) };

// Spy - tracks calls to real implementation
const spy = jest.spyOn(service, 'validate');

// Fake - simplified working implementation
class FakeEmailService {
  sent: Email[] = [];
  async send(email: Email) { this.sent.push(email); }
}

// Reset between tests
beforeEach(() => jest.clearAllMocks());
```

---

## Human Documentation

### When to Apply

- Isolating unit tests from external dependencies
- Testing code that calls APIs, databases, or file systems
- Controlling non-deterministic behavior (time, random)
- Verifying interactions with dependencies

### Implementation Guide

#### 1. Mock vs Stub vs Spy vs Fake

**Stub**: Pre-programmed return values
```typescript
const userRepo = {
  findById: jest.fn().mockResolvedValue({ id: '1', name: 'John' })
};
```

**Mock**: Stubs + verification
```typescript
const emailService = {
  send: jest.fn().mockResolvedValue(true)
};

// After test
expect(emailService.send).toHaveBeenCalledWith({
  to: 'user@example.com',
  subject: 'Welcome'
});
```

**Spy**: Wraps real implementation
```typescript
const spy = jest.spyOn(console, 'log');
doSomething();
expect(spy).toHaveBeenCalledWith('expected message');
spy.mockRestore();
```

**Fake**: Simplified working implementation
```typescript
class FakeUserRepository implements UserRepository {
  private users = new Map<string, User>();

  async save(user: User): Promise<User> {
    const id = user.id || crypto.randomUUID();
    const saved = { ...user, id };
    this.users.set(id, saved);
    return saved;
  }

  async findById(id: string): Promise<User | null> {
    return this.users.get(id) ?? null;
  }
}
```

#### 2. What to Mock

**DO Mock**:
- External APIs and services
- Database calls
- File system operations
- Network requests
- Time/date operations
- Random number generation

**DON'T Mock**:
- The code under test
- Simple value objects
- Pure utility functions
- Dependencies that are fast and deterministic

#### 3. Mock Patterns

```typescript
// Module mock
jest.mock('./database');

// Partial mock
jest.mock('./utils', () => ({
  ...jest.requireActual('./utils'),
  fetchData: jest.fn()
}));

// Sequential returns
mockFn
  .mockResolvedValueOnce(firstResult)
  .mockResolvedValueOnce(secondResult)
  .mockRejectedValueOnce(new Error('fail'));

// Implementation mock
mockFn.mockImplementation((x) => x * 2);
```

#### 4. Cleanup

```typescript
beforeEach(() => {
  jest.clearAllMocks();  // Clear call history
});

afterEach(() => {
  jest.restoreAllMocks(); // Restore spies
});
```

### Anti-Patterns

- Mocking everything (makes tests brittle)
- Not resetting mocks between tests
- Mocking the system under test
- Over-specifying mock behavior
- Ignoring mock verification

### Examples

See `SKILL.md` for comprehensive examples.
