---
name: Type Safety
category: Java
tags: [java, optional, nullable, null-safety, annotations]
activation:
  keywords: [optional, nullable, null, nonnull, requirenonnull]
  file_patterns: ["**/*.java"]
---

# Type Safety Pattern

## AI Quick Reference

**Purpose**: Ensure null safety and explicit handling of absent values in Java code.

**Key Rules**:
1. Use `Optional<T>` for return values that may be absent
2. Never use `Optional` as method parameter or field
3. Use `@Nullable`/`@NonNull` annotations for method parameters
4. Validate non-null parameters with `Objects.requireNonNull()`
5. Prefer `orElseGet()` over `orElse()` for expensive defaults

**Quick Patterns**:

```java
// Optional return value
public Optional<User> findById(String id) {
    return Optional.ofNullable(repository.findById(id));
}

// Null annotations on parameters
public User createUser(@NonNull String name, @Nullable String email) {
    Objects.requireNonNull(name, "name cannot be null");
    return new User(name, email);
}

// Safe Optional consumption
String email = findById(id)
    .map(User::getEmail)
    .orElse("unknown@example.com");
```

---

## Human Documentation

### When to Apply

- Designing public API methods that may return absent values
- Accepting parameters that could be null
- Constructor dependency injection with validation
- Working with collections that may contain null elements

### Implementation Guide

#### 1. Optional for Return Values

Use `Optional<T>` when a method may legitimately return no value:

```java
// Good - explicit absence
public Optional<User> findByEmail(String email) {
    User user = userRepository.findByEmail(email);
    return Optional.ofNullable(user);
}

// Usage
findByEmail(email)
    .map(User::getName)
    .ifPresent(name -> log.info("Found user: {}", name));
```

#### 2. Null Safety Annotations

Use JSpecify, Checker Framework, or JetBrains annotations:

```java
import org.jspecify.annotations.Nullable;
import org.jspecify.annotations.NonNull;

public class UserService {
    // @NonNull is the default for return types
    public @NonNull User getOrCreate(@NonNull String id, @Nullable String name) {
        return findById(id).orElseGet(() -> createUser(id, name));
    }
}
```

#### 3. Defensive Constructor Validation

```java
public class OrderService {
    private final OrderRepository repository;
    private final PaymentService paymentService;
    private final NotificationService notificationService;

    public OrderService(
            OrderRepository repository,
            PaymentService paymentService,
            NotificationService notificationService) {
        this.repository = Objects.requireNonNull(repository, "repository");
        this.paymentService = Objects.requireNonNull(paymentService, "paymentService");
        this.notificationService = Objects.requireNonNull(notificationService, "notificationService");
    }
}
```

#### 4. Optional Transformation Chains

```java
// Chain transformations safely
String city = findUserById(id)
    .map(User::getAddress)
    .map(Address::getCity)
    .map(String::toUpperCase)
    .orElse("UNKNOWN");

// Use flatMap for Optional-returning methods
Optional<Order> latestOrder = findUserById(id)
    .flatMap(User::getLatestOrder);
```

### Anti-Patterns

- Using `Optional.get()` without checking `isPresent()`
- Storing `Optional` in fields or using as method parameters
- Using `orElse()` with expensive computations (use `orElseGet()`)
- Returning `null` from methods that could return `Optional`
- Nesting Optional (`Optional<Optional<T>>`)

### Examples

See `SKILL.md` for comprehensive examples and the null handling section.
