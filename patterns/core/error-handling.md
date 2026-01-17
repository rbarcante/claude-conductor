---
name: "Error Handling"
category: "Resilience"
tags:
  - errors
  - exceptions
  - fault-tolerance
  - user-experience
activation:
  keywords:
    - error
    - exception
    - catch
    - throw
    - try
    - handle
    - fault
    - failure
  file_patterns:
    - "**/error*.{js,ts,py,go,rs,java,kt}"
    - "**/exception*.{js,ts,py,go,rs,java,kt}"
    - "**/*Exception.java"
    - "**/*Error.java"
version: "1.0"
last_updated: "2026-01-19"
---

# Error Handling

> Implement robust error handling with clear propagation, meaningful messages, and graceful degradation.

---

## AI Quick Reference

### When to Apply
- Implementing any operation that can fail (I/O, network, parsing)
- Creating APIs or public interfaces
- Building user-facing features that need graceful failure
- Wrapping external dependencies

### Core Principles
1. **Fail Fast**: Detect and report errors as early as possible
2. **Be Specific**: Use typed/custom errors over generic ones
3. **Preserve Context**: Include relevant data in error messages
4. **User vs Developer**: Separate user-facing messages from technical details
5. **Recover Gracefully**: Provide fallbacks when possible

### Quick Implementation Checklist
- [ ] Define custom error types for domain-specific failures
- [ ] Include error codes for programmatic handling
- [ ] Log technical details, show friendly messages to users
- [ ] Clean up resources in finally/defer blocks
- [ ] Document which errors each function can throw/return

### Code Pattern (Pseudocode)
```
// Structured error with context
class DomainError {
    code: string      // "USER_NOT_FOUND"
    message: string   // Technical message for logs
    userMessage: string  // Safe message for UI
    context: object   // Relevant data for debugging
    cause: Error      // Original error if wrapping
}

function riskyOperation() {
    try {
        result = attemptOperation()
        return result
    } catch (error) {
        log.error("Operation failed", { error, context })
        throw new DomainError({
            code: "OPERATION_FAILED",
            message: error.message,
            userMessage: "Something went wrong. Please try again.",
            cause: error
        })
    } finally {
        cleanup()
    }
}
```

### Key Decisions
| Decision Point | Recommended Choice | Rationale |
|----------------|-------------------|-----------|
| Error representation | Custom error types | Enables type-safe handling |
| Error propagation | Wrap and rethrow | Preserves stack trace + adds context |
| User messages | Separate from technical | Security + UX |
| Logging | Always log before handling | Ensures visibility |

---

## Human Documentation

### Overview

Error handling is fundamental to building reliable software. Poor error handling leads to silent failures, confusing user experiences, and difficult debugging. This pattern establishes a consistent approach to detecting, reporting, and recovering from errors.

The goal is to create a system where:
- Errors are caught at appropriate boundaries
- Technical details are logged for debugging
- Users receive helpful, actionable messages
- Resources are properly cleaned up
- The system degrades gracefully when possible

### Detailed Explanation

#### Concept 1: Error Boundaries

Error boundaries are the points in your code where errors should be caught and handled. Not every function needs try/catch—errors should bubble up to appropriate boundaries:

- **API/Controller Layer**: Catch and transform errors into HTTP responses
- **Service Layer**: Catch and wrap external service failures
- **Repository Layer**: Catch and wrap database errors
- **UI Layer**: Catch and display user-friendly messages

#### Concept 2: Error Classification

Errors should be classified by their nature and handling requirements:

| Type | Example | Handling |
|------|---------|----------|
| **Validation** | Invalid email format | Return to user with guidance |
| **Business Logic** | Insufficient funds | Return to user with explanation |
| **Infrastructure** | Database timeout | Retry, then fail gracefully |
| **Programming** | Null pointer | Log, alert developers |
| **External** | Third-party API down | Circuit breaker, fallback |

#### Concept 3: Error Context

Every error should carry enough context to understand what happened:

```
{
    code: "PAYMENT_FAILED",
    message: "Stripe API returned 402: card_declined",
    userMessage: "Your payment was declined. Please try a different card.",
    context: {
        userId: "user_123",
        amount: 99.99,
        currency: "USD",
        stripeErrorCode: "card_declined"
    },
    timestamp: "2026-01-19T12:00:00Z",
    requestId: "req_abc123"
}
```

### Implementation Examples

#### Example 1: Basic Error Wrapper

```typescript
// Define domain errors
class AppError extends Error {
    constructor(
        public code: string,
        public message: string,
        public userMessage: string,
        public statusCode: number = 500,
        public cause?: Error
    ) {
        super(message);
        this.name = 'AppError';
    }
}

// Usage
async function getUser(id: string): Promise<User> {
    try {
        const user = await db.users.findById(id);
        if (!user) {
            throw new AppError(
                'USER_NOT_FOUND',
                `User with id ${id} not found in database`,
                'User not found',
                404
            );
        }
        return user;
    } catch (error) {
        if (error instanceof AppError) throw error;
        throw new AppError(
            'DATABASE_ERROR',
            error.message,
            'Unable to fetch user. Please try again.',
            500,
            error
        );
    }
}
```

#### Example 2: Result Type Pattern (No Exceptions)

```typescript
type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

function parseConfig(raw: string): Result<Config, ParseError> {
    try {
        const config = JSON.parse(raw);
        if (!isValidConfig(config)) {
            return { ok: false, error: new ParseError('Invalid config structure') };
        }
        return { ok: true, value: config };
    } catch (e) {
        return { ok: false, error: new ParseError('Invalid JSON') };
    }
}

// Usage - forces explicit error handling
const result = parseConfig(rawConfig);
if (!result.ok) {
    log.warn('Config parse failed', { error: result.error });
    return defaultConfig;
}
return result.value;
```

### Best Practices

1. **Never Swallow Errors Silently**: Even if you can recover, log the error for visibility.

2. **Use Error Codes**: String or numeric codes enable programmatic handling and i18n.

3. **Sanitize User Messages**: Never expose stack traces, SQL queries, or internal paths to users.

4. **Include Request IDs**: Correlate user-reported errors with server logs.

5. **Test Error Paths**: Write tests that verify error handling, not just happy paths.

### Trade-offs and Considerations

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| Exceptions | Natural flow, built-in | Hidden control flow, performance | Most languages/scenarios |
| Result types | Explicit, type-safe | Verbose, requires discipline | Functional style, critical paths |
| Error callbacks | Flexible, composable | Callback hell, easy to forget | Legacy APIs, event-driven |
| Global handler | Catches everything | Can mask issues | Last-resort safety net |

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Pokemon Exception Handling

**What it looks like:**
```javascript
try {
    doSomething();
} catch (e) {
    // Gotta catch 'em all!
}
```

**Why it's problematic:**
- Silently swallows all errors including programming bugs
- Makes debugging nearly impossible
- Hides real issues until they become critical

**Better approach:**
```javascript
try {
    doSomething();
} catch (e) {
    log.error('doSomething failed', { error: e });
    if (e instanceof ExpectedError) {
        return fallbackValue;
    }
    throw e; // Re-throw unexpected errors
}
```

### Anti-Pattern 2: String-Based Error Checking

**What it looks like:**
```javascript
try {
    await saveUser(user);
} catch (e) {
    if (e.message.includes('duplicate key')) {
        // Handle duplicate...
    }
}
```

**Why it's problematic:**
- Fragile—message wording can change
- Not type-safe
- Different databases use different messages

**Better approach:**
```javascript
try {
    await saveUser(user);
} catch (e) {
    if (e.code === 'DUPLICATE_KEY' || e.code === '23505') {
        // Handle duplicate using error codes
    }
}
```

### Anti-Pattern 3: Exposing Internal Errors to Users

**What it looks like:**
```javascript
app.use((err, req, res, next) => {
    res.status(500).json({ error: err.stack });
});
```

**Why it's problematic:**
- Security risk: exposes file paths, library versions
- Poor UX: technical jargon confuses users
- Privacy risk: may expose other users' data in context

**Better approach:**
```javascript
app.use((err, req, res, next) => {
    const requestId = req.id;
    log.error('Request failed', { requestId, error: err });
    res.status(err.statusCode || 500).json({
        error: err.userMessage || 'An unexpected error occurred',
        requestId: requestId // Helps users report issues
    });
});
```

---

## Related Patterns

- [Logging](./logging.md) - How to log errors effectively
- [Validation](./validation.md) - Preventing errors through input validation

---

## References

- [Error Handling Best Practices](https://www.toptal.com/qa/how-to-write-testable-code-and-why-it-matters) - General principles
- [Node.js Error Handling](https://nodejs.org/api/errors.html) - Node-specific guidance
- [Go Error Handling](https://go.dev/blog/error-handling-and-go) - Go's explicit approach
