---
name: "Logging"
category: "Observability"
tags:
  - logging
  - debugging
  - monitoring
  - observability
activation:
  keywords:
    - log
    - logging
    - logger
    - debug
    - info
    - warn
    - trace
    - audit
    - telemetry
  file_patterns:
    - "**/log*.{js,ts,py,go,rs,java,kt}"
    - "**/logger*.{js,ts,py,go,rs,java,kt}"
    - "**/*Logger.java"
    - "**/Log*.java"
version: "1.0"
last_updated: "2026-01-19"
---

# Logging

> Implement structured, leveled logging with contextual information for debugging, monitoring, and auditing.

---

## AI Quick Reference

### When to Apply
- Starting any new service or application
- Adding observability to existing code
- Debugging production issues
- Meeting compliance/audit requirements
- Implementing error handling (log before handle)

### Core Principles
1. **Use Log Levels**: DEBUG < INFO < WARN < ERROR < FATAL
2. **Structured Format**: Use JSON or key-value pairs, not plain text
3. **Include Context**: Request ID, user ID, operation name
4. **Never Log Secrets**: Mask passwords, tokens, PII
5. **Log at Boundaries**: Entry/exit of services, not every function

### Quick Implementation Checklist
- [ ] Choose a structured logging library (not console.log)
- [ ] Define log levels for your environment (DEBUG in dev, INFO in prod)
- [ ] Add request/correlation IDs to all logs
- [ ] Create sensitive data filters
- [ ] Set up log aggregation (ELK, Datadog, etc.)
- [ ] Document what each log level means for your team

### Code Pattern (Pseudocode)
```
// Initialize logger with context
logger = createLogger({
    level: env.LOG_LEVEL || 'info',
    format: 'json',
    defaultMeta: { service: 'user-service', version: '1.0.0' }
})

// Create child logger with request context
function handleRequest(req) {
    reqLogger = logger.child({
        requestId: req.id,
        userId: req.user?.id,
        path: req.path
    })

    reqLogger.info('Request started')

    try {
        result = processRequest(req)
        reqLogger.info('Request completed', { status: 'success' })
        return result
    } catch (error) {
        reqLogger.error('Request failed', {
            error: error.message,
            stack: error.stack
        })
        throw error
    }
}
```

### Key Decisions
| Decision Point | Recommended Choice | Rationale |
|----------------|-------------------|-----------|
| Format | JSON structured | Machine parseable, searchable |
| Log library | Dedicated (winston, pino, zerolog) | Features, performance |
| Level in prod | INFO or WARN | Reduce noise, cost |
| Correlation | Request ID header | Trace across services |

---

## Human Documentation

### Overview

Logging is essential for understanding what your application is doing in production. Good logging practices enable quick debugging, performance monitoring, security auditing, and compliance reporting.

The goal is to create logs that:
- Tell a story of what happened
- Can be searched and filtered efficiently
- Don't expose sensitive information
- Don't degrade application performance
- Provide enough context to debug issues

### Detailed Explanation

#### Concept 1: Log Levels

Log levels indicate the severity and importance of a message:

| Level | When to Use | Example |
|-------|-------------|---------|
| **TRACE** | Very detailed debugging | Function entry/exit |
| **DEBUG** | Diagnostic information | Variable values, state changes |
| **INFO** | Normal operations | Request received, job started |
| **WARN** | Potential problems | Deprecated API used, retry needed |
| **ERROR** | Failures that need attention | Request failed, connection lost |
| **FATAL** | Application cannot continue | Missing config, database unreachable |

**Rule of thumb**: In production, you should be able to understand the system's behavior from INFO logs alone. DEBUG should add detail, not context.

#### Concept 2: Structured Logging

Structured logs use consistent key-value pairs instead of free-form text:

**Unstructured (bad):**
```
[2026-01-19 12:00:00] User john@example.com logged in from 192.168.1.1
```

**Structured (good):**
```json
{
  "timestamp": "2026-01-19T12:00:00Z",
  "level": "info",
  "message": "User logged in",
  "userId": "user_123",
  "email": "j***@example.com",
  "ip": "192.168.1.1",
  "userAgent": "Mozilla/5.0..."
}
```

Benefits:
- Searchable: `userId:user_123 AND level:error`
- Aggregatable: Count logins per hour
- Parseable: Automated alerting rules

#### Concept 3: Contextual Logging

Every log entry should include enough context to understand it in isolation:

```json
{
  "timestamp": "2026-01-19T12:00:00Z",
  "level": "error",
  "message": "Payment processing failed",
  "service": "payment-service",
  "version": "2.3.1",
  "environment": "production",
  "requestId": "req_abc123",
  "traceId": "trace_xyz789",
  "userId": "user_456",
  "orderId": "order_789",
  "amount": 99.99,
  "currency": "USD",
  "errorCode": "INSUFFICIENT_FUNDS",
  "duration_ms": 234
}
```

### Implementation Examples

#### Example 1: Logger Setup with Configuration

```
// Create base logger with configuration
logger = createLogger({
    level: environment.LOG_LEVEL or "info",
    format: "json",
    redactPaths: ["password", "token", "authorization", "*.password"],
    redactValue: "[REDACTED]",
    defaultContext: {
        service: environment.SERVICE_NAME,
        version: environment.APP_VERSION,
        env: environment.NODE_ENV
    }
})

// Request logging middleware
function requestLoggerMiddleware(request, response, next):
    // Create child logger with request context
    request.logger = logger.createChild({
        requestId: request.id,
        method: request.method,
        path: request.path,
        userId: request.user?.id
    })

    startTime = currentTimeMillis()

    // Log when response finishes
    response.onFinish(function():
        request.logger.info("Request completed", {
            statusCode: response.statusCode,
            duration_ms: currentTimeMillis() - startTime
        })
    )

    next()
```

#### Example 2: Sensitive Data Sanitization

```
// Define sensitive field patterns
sensitiveFields = ["password", "token", "ssn", "creditCard", "secret"]

function sanitizeForLogging(data):
    sanitized = copy(data)

    for key in sanitized.keys():
        // Check if field name matches sensitive patterns
        if anySensitiveFieldMatches(key, sensitiveFields):
            sanitized[key] = "[REDACTED]"

        // Partially mask email addresses
        else if key == "email" and sanitized[key] is not null:
            localPart, domain = sanitized[key].split("@")
            sanitized[key] = localPart[0] + "***@" + domain

        // Recursively sanitize nested objects
        else if sanitized[key] is object:
            sanitized[key] = sanitizeForLogging(sanitized[key])

    return sanitized

// Usage
logger.info("Processing user data", sanitizeForLogging(userInput))
```

### Best Practices

1. **Use Correlation IDs**: Pass a unique ID through all services handling a request. Use headers like `X-Request-ID` or `X-Correlation-ID`.

2. **Log at Service Boundaries**: Log when entering/exiting your service, not inside every function. Internal tracing should use TRACE/DEBUG levels.

3. **Include Timing Information**: Log duration of operations for performance monitoring.

4. **Separate Application and Access Logs**: HTTP access logs (nginx-style) serve different purposes than application logs.

5. **Use Sampling for High-Volume Logs**: In high-throughput systems, sample DEBUG logs (e.g., log 1% of requests at DEBUG level).

### Trade-offs and Considerations

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| JSON structured | Searchable, parseable | Larger size, less human-readable | Production systems |
| Plain text | Human-readable, simple | Hard to parse/search | Local development |
| Log aggregation service | Powerful search, alerts | Cost, complexity | Production at scale |
| File-based logs | Simple, no dependencies | Hard to search, rotation needed | Small deployments |

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Logging Sensitive Data

**What it looks like:**
```
logger.info("User login", {
    email: user.email,
    password: user.password,  // NEVER!
    token: authToken          // NEVER!
})
```

**Why it's problematic:**
- Security breach if logs are exposed
- Compliance violations (GDPR, PCI-DSS)
- Logs often have broader access than databases

**Better approach:**
```
logger.info("User login", {
    userId: user.id,
    email: maskEmail(user.email),
    // password: NEVER LOG
    tokenId: authToken.id  // Log identifier, not value
})
```

### Anti-Pattern 2: Print Statements in Production

**What it looks like:**
```
print("Processing order: " + orderId)
print("User data: " + toJson(user))
```

**Why it's problematic:**
- No log levels
- No structure
- No context
- Performance impact (often synchronous)
- Often left in accidentally

**Better approach:**
```
logger.info("Processing order", orderId = orderId)
logger.debug("User data loaded", user = sanitize(user))
```

### Anti-Pattern 3: Logging Everything

**What it looks like:**
```
function calculateTotal(items):
    logger.debug("Entering calculateTotal")
    logger.debug("Items: " + items)
    total = 0
    for item in items:
        logger.debug("Processing item: " + item)
        total = total + item.price
        logger.debug("Running total: " + total)
    logger.debug("Exiting calculateTotal")
    return total
```

**Why it's problematic:**
- Log volume explodes (cost, storage)
- Important logs buried in noise
- Performance degradation
- Difficult to find relevant information

**Better approach:**
```
function calculateTotal(items):
    logger.debug("Calculating order total", itemCount = items.length)
    total = sum(item.price for item in items)
    logger.debug("Order total calculated", total = total)
    return total
```

---

## Related Patterns

- [Error Handling](./error-handling.md) - Log errors before handling
- [Configuration](./configuration.md) - Configure log levels per environment

---

## References

- [12 Factor App - Logs](https://12factor.net/logs) - Treat logs as event streams
- [OpenTelemetry Logging](https://opentelemetry.io/) - Modern observability standards
- [OWASP Logging Guide](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) - Security considerations
