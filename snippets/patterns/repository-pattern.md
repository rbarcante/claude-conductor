---
use: When abstracting data access to decouple business logic from storage implementation
requires: Understanding of interfaces/protocols in your language
pattern: Configuration, Data Integrity
---

# Repository Pattern

Abstracts data access behind a consistent interface, enabling testable business logic and interchangeable storage backends.

## AI Quick Reference

### When to Apply
- Business logic needs to access persistent data
- You want to unit test without a real database
- Multiple storage backends are possible (SQL, NoSQL, API)
- Domain objects should be storage-agnostic

### Core Structure
```
┌─────────────────┐     ┌───────────────────┐
│  Business Logic │────>│  IRepository<T>   │ (interface)
└─────────────────┘     └───────────────────┘
                               ▲
                 ┌─────────────┼─────────────┐
                 │             │             │
        ┌────────┴───┐  ┌──────┴────┐  ┌─────┴─────┐
        │ SqlRepo    │  │ MongoRepo │  │ MockRepo  │
        └────────────┘  └───────────┘  └───────────┘
```

### Key Methods
| Method | Purpose |
|--------|---------|
| `get_by_id(id)` | Fetch single entity |
| `get_all()` | Fetch all entities |
| `find(criteria)` | Query with filters |
| `save(entity)` | Insert or update |
| `delete(id)` | Remove entity |

---

## TypeScript Implementation

```typescript
// Interface
interface IRepository<T, ID = string> {
  getById(id: ID): Promise<T | null>;
  getAll(): Promise<T[]>;
  find(criteria: Partial<T>): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: ID): Promise<boolean>;
}

// Domain entity
interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

// CUSTOMIZE: Implement for your storage
class PostgresUserRepository implements IRepository<User> {
  constructor(private db: DatabaseConnection) {}

  async getById(id: string): Promise<User | null> {
    const row = await this.db.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return row ? this.mapToUser(row) : null;
  }

  async getAll(): Promise<User[]> {
    const rows = await this.db.query('SELECT * FROM users');
    return rows.map(this.mapToUser);
  }

  async find(criteria: Partial<User>): Promise<User[]> {
    // Build dynamic query from criteria
    const conditions = Object.entries(criteria)
      .map(([key, _], i) => `${key} = $${i + 1}`);
    const values = Object.values(criteria);

    const rows = await this.db.query(
      `SELECT * FROM users WHERE ${conditions.join(' AND ')}`,
      values
    );
    return rows.map(this.mapToUser);
  }

  async save(user: User): Promise<User> {
    const result = await this.db.query(
      `INSERT INTO users (id, email, name, created_at)
       VALUES ($1, $2, $3, $4)
       ON CONFLICT (id) DO UPDATE SET email = $2, name = $3
       RETURNING *`,
      [user.id, user.email, user.name, user.createdAt]
    );
    return this.mapToUser(result);
  }

  async delete(id: string): Promise<boolean> {
    const result = await this.db.query(
      'DELETE FROM users WHERE id = $1',
      [id]
    );
    return result.rowCount > 0;
  }

  private mapToUser(row: any): User {
    return {
      id: row.id,
      email: row.email,
      name: row.name,
      createdAt: new Date(row.created_at),
    };
  }
}

// In-memory for testing
class InMemoryUserRepository implements IRepository<User> {
  private users = new Map<string, User>();

  async getById(id: string): Promise<User | null> {
    return this.users.get(id) ?? null;
  }

  async getAll(): Promise<User[]> {
    return Array.from(this.users.values());
  }

  async find(criteria: Partial<User>): Promise<User[]> {
    return Array.from(this.users.values()).filter(user =>
      Object.entries(criteria).every(([key, value]) =>
        user[key as keyof User] === value
      )
    );
  }

  async save(user: User): Promise<User> {
    this.users.set(user.id, user);
    return user;
  }

  async delete(id: string): Promise<boolean> {
    return this.users.delete(id);
  }
}
```

## Python Implementation

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Generic, TypeVar, Protocol

T = TypeVar("T")
ID = TypeVar("ID")


class Repository(ABC, Generic[T, ID]):
    """Abstract repository interface."""

    @abstractmethod
    async def get_by_id(self, id: ID) -> T | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[T]:
        pass

    @abstractmethod
    async def find(self, **criteria) -> list[T]:
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        pass

    @abstractmethod
    async def delete(self, id: ID) -> bool:
        pass


@dataclass
class User:
    id: str
    email: str
    name: str
    created_at: datetime


# CUSTOMIZE: Implement for your storage
class PostgresUserRepository(Repository[User, str]):
    def __init__(self, db):
        self.db = db

    async def get_by_id(self, id: str) -> User | None:
        row = await self.db.fetchone(
            "SELECT * FROM users WHERE id = $1", id
        )
        return self._map_to_user(row) if row else None

    async def get_all(self) -> list[User]:
        rows = await self.db.fetch("SELECT * FROM users")
        return [self._map_to_user(row) for row in rows]

    async def find(self, **criteria) -> list[User]:
        conditions = " AND ".join(f"{k} = ${i+1}" for i, k in enumerate(criteria))
        rows = await self.db.fetch(
            f"SELECT * FROM users WHERE {conditions}",
            *criteria.values()
        )
        return [self._map_to_user(row) for row in rows]

    async def save(self, user: User) -> User:
        await self.db.execute(
            """INSERT INTO users (id, email, name, created_at)
               VALUES ($1, $2, $3, $4)
               ON CONFLICT (id) DO UPDATE SET email = $2, name = $3""",
            user.id, user.email, user.name, user.created_at
        )
        return user

    async def delete(self, id: str) -> bool:
        result = await self.db.execute(
            "DELETE FROM users WHERE id = $1", id
        )
        return result == "DELETE 1"

    def _map_to_user(self, row) -> User:
        return User(
            id=row["id"],
            email=row["email"],
            name=row["name"],
            created_at=row["created_at"],
        )


# In-memory for testing
class InMemoryUserRepository(Repository[User, str]):
    def __init__(self):
        self._users: dict[str, User] = {}

    async def get_by_id(self, id: str) -> User | None:
        return self._users.get(id)

    async def get_all(self) -> list[User]:
        return list(self._users.values())

    async def find(self, **criteria) -> list[User]:
        return [
            u for u in self._users.values()
            if all(getattr(u, k) == v for k, v in criteria.items())
        ]

    async def save(self, user: User) -> User:
        self._users[user.id] = user
        return user

    async def delete(self, id: str) -> bool:
        if id in self._users:
            del self._users[id]
            return True
        return False
```

## Best Practices

1. **Keep repositories focused** - One repository per aggregate root
2. **Return domain objects** - Not database rows or ORMs
3. **Use dependency injection** - Inject repository interface, not implementation
4. **Avoid business logic** - Repositories handle data access only
5. **Test with in-memory** - Fast unit tests without database
