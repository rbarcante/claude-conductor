# Snippet Library

Production-ready code snippets with AI-optimized headers for quick reference and insertion.

## Usage

Use the `/conductor:snippet` command to browse and insert snippets:

```bash
/conductor:snippet list              # List all snippets by category
/conductor:snippet search <query>    # Search snippets by keyword
/conductor:snippet show <name>       # Display a specific snippet
```

## Snippet Format

Each snippet includes:
- **AI Header**: Structured comment with USE, REQUIRES, and PATTERN metadata
- **Complete Code**: Production-ready, runnable implementation
- **Customization Points**: Inline comments marking where to adapt

## Categories

### TypeScript

| Snippet | Description | Pattern |
|---------|-------------|---------|
| [api-client.ts](./typescript/api-client.ts) | Type-safe HTTP client with error handling | Error Handling, Configuration |
| [error-handler.ts](./typescript/error-handler.ts) | Custom error types and global handler | Error Handling |
| [type-guard.ts](./typescript/type-guard.ts) | Runtime type validation utilities | Validation |
| [async-wrapper.ts](./typescript/async-wrapper.ts) | Async operation with retry and timeout | Error Handling, Resilience |
| [config-loader.ts](./typescript/config-loader.ts) | Environment-based configuration loading | Configuration |

### Python

| Snippet | Description | Pattern |
|---------|-------------|---------|
| [api-client.py](./python/api-client.py) | HTTP client with retries using httpx | Error Handling, Configuration |
| [error-handler.py](./python/error-handler.py) | Custom exception hierarchy with context | Error Handling |
| [dependency-injection.py](./python/dependency-injection.py) | Simple DI container implementation | Configuration |
| [config-loader.py](./python/config-loader.py) | Pydantic-based configuration with validation | Configuration, Validation |
| [async-patterns.py](./python/async-patterns.py) | Async/await patterns with error handling | Error Handling, Resilience |

### Java

| Snippet | Description | Pattern |
|---------|-------------|---------|
| [api-client.java](./java/api-client.java) | Type-safe HTTP client using HttpClient (Java 11+) | Error Handling, Configuration |
| [error-handler.java](./java/error-handler.java) | Custom exception hierarchy with error codes | Error Handling |
| [dependency-injection.java](./java/dependency-injection.java) | Spring/Jakarta DI patterns with configuration | Configuration |

### Patterns

| Snippet | Description | Language |
|---------|-------------|----------|
| [repository-pattern.md](./patterns/repository-pattern.md) | Data access abstraction | Language-agnostic |
| [factory-pattern.md](./patterns/factory-pattern.md) | Object creation patterns | Language-agnostic |

## Contributing Snippets

1. Create snippet file in appropriate category directory
2. Include AI header comment block:
   ```
   /**
    * USE: Brief description of when to use this snippet
    * REQUIRES: Dependencies or prerequisites
    * PATTERN: Related patterns from Pattern Reference Layer
    */
   ```
3. Ensure code is complete and production-ready
4. Mark customization points with `// CUSTOMIZE:` comments
5. Add entry to this index

## AI Header Format

### TypeScript/JavaScript
```typescript
/**
 * USE: When you need [specific use case]
 * REQUIRES: [dependencies, e.g., "fetch API", "Node.js 18+"]
 * PATTERN: [related patterns, e.g., "Error Handling", "Configuration"]
 */
```

### Python
```python
"""
USE: When you need [specific use case]
REQUIRES: [dependencies, e.g., "httpx>=0.24", "pydantic>=2.0"]
PATTERN: [related patterns, e.g., "Error Handling", "Configuration"]
"""
```

### Java
```java
/**
 * USE: When you need [specific use case]
 * REQUIRES: [dependencies, e.g., "Java 17+", "Spring Boot 3.x"]
 * PATTERN: [related patterns, e.g., "Error Handling", "Configuration"]
 */
```

### Markdown (Pattern snippets)
```markdown
---
use: When you need [specific use case]
requires: [prerequisites]
pattern: [related patterns]
---
```
