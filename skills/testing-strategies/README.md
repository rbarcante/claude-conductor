# Testing Strategies Skill

A Conductor skill providing guidance for writing effective, maintainable tests.

## Overview

This skill activates when working with test files and provides guidance on:

- **Unit Testing**: Structure, assertions, edge cases
- **Integration Testing**: Database, API, service integration
- **Mocking**: When and how to mock dependencies

## Activation

The skill automatically activates when:

- Working with files in `test/`, `tests/`, or `__tests__/` directories
- Working with files matching `*.test.*` or `*.spec.*`
- Task description contains keywords: `test`, `unit`, `integration`, `mock`
- Project uses testing tools (Jest, Vitest, Pytest, etc.)

## Patterns Provided

| Pattern | Description |
|---------|-------------|
| [unit-test-patterns](patterns/unit-test-patterns.md) | Structure, naming, assertions |
| [integration-patterns](patterns/integration-patterns.md) | Database, API, service tests |
| [mocking-strategies](patterns/mocking-strategies.md) | When and how to mock |

## Usage Examples

### Unit Test with Mocks

```typescript
import { UserService } from '../services/user';
import { UserRepository } from '../repositories/user';

describe('UserService', () => {
  let service: UserService;
  let mockRepo: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepo = {
      findById: jest.fn(),
      save: jest.fn(),
      delete: jest.fn()
    };
    service = new UserService(mockRepo);
  });

  describe('getUser', () => {
    it('should return user when found', async () => {
      // Arrange
      const mockUser = { id: '1', name: 'John' };
      mockRepo.findById.mockResolvedValue(mockUser);

      // Act
      const result = await service.getUser('1');

      // Assert
      expect(result).toEqual(mockUser);
      expect(mockRepo.findById).toHaveBeenCalledWith('1');
    });

    it('should return null when not found', async () => {
      // Arrange
      mockRepo.findById.mockResolvedValue(null);

      // Act
      const result = await service.getUser('999');

      // Assert
      expect(result).toBeNull();
    });
  });
});
```

### Integration Test with Database

```typescript
import { createTestDatabase, clearDatabase } from '../helpers/test-db';
import { UserRepository } from '../repositories/user';

describe('UserRepository Integration', () => {
  let db: Database;
  let repo: UserRepository;

  beforeAll(async () => {
    db = await createTestDatabase();
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    await clearDatabase(db);
    repo = new UserRepository(db);
  });

  it('should persist and retrieve user', async () => {
    // Create user
    const created = await repo.create({
      name: 'John',
      email: 'john@example.com'
    });

    expect(created.id).toBeDefined();

    // Retrieve user
    const found = await repo.findById(created.id);

    expect(found).toEqual(created);
  });
});
```

### API Integration Test

```typescript
import request from 'supertest';
import { createApp } from '../app';

describe('Users API', () => {
  const app = createApp();

  describe('POST /api/v1/users', () => {
    it('should create user with valid data', async () => {
      const response = await request(app)
        .post('/api/v1/users')
        .send({
          name: 'John Doe',
          email: 'john@example.com'
        });

      expect(response.status).toBe(201);
      expect(response.body.data).toMatchObject({
        name: 'John Doe',
        email: 'john@example.com'
      });
    });

    it('should return 422 for invalid data', async () => {
      const response = await request(app)
        .post('/api/v1/users')
        .send({
          name: 'John Doe',
          email: 'not-an-email'
        });

      expect(response.status).toBe(422);
      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
  });
});
```

## Best Practices

1. **One concept per test** - Each test should verify one thing
2. **Descriptive names** - Test names should describe expected behavior
3. **AAA pattern** - Arrange, Act, Assert in every test
4. **Independent tests** - No shared state between tests
5. **Fast unit tests** - Keep unit tests under 100ms each

## Related Skills

- **typescript-best-practices**: For typed test code
- **api-design**: For API testing patterns

## Changelog

### 1.0.0

- Initial release
- Unit test patterns
- Integration patterns
- Mocking strategies
