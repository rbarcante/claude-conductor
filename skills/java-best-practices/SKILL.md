---
name: java-best-practices
description: Use this skill when working with Java code, Optional handling, CompletableFuture, records, sealed classes, or virtual threads.
version: 1.0.0
---

# Java Best Practices

Guidance for writing type-safe, concurrent, and modern Java code targeting Java 17+ and Java 21 LTS. Covers null safety, concurrency patterns, and modern language features.

## Core Principles

1. **Null safety first**: Use Optional for return values, @Nullable/@NonNull for parameters
2. **Immutability preferred**: Use records for data carriers, final fields where possible
3. **Explicit error handling**: Use checked exceptions sparingly, prefer Result patterns
4. **Modern features**: Leverage records, sealed classes, and pattern matching
5. **Virtual threads for IO**: Use virtual threads (Java 21) for IO-bound operations

## Type Safety

### Use Optional for Return Values

```java
// Good - explicit absence representation
public Optional<User> findById(String id) {
    User user = userRepository.findById(id);
    return Optional.ofNullable(user);
}

// Bad - null return
public User findById(String id) {
    return userRepository.findById(id); // May return null
}
```

### Never Use Optional as Parameter or Field

```java
// Bad - Optional as parameter
public void processUser(Optional<User> user) { ... }

// Good - use @Nullable annotation or overloading
public void processUser(@Nullable User user) { ... }
public void processUser(User user) { ... } // Overload for non-null

// Bad - Optional as field
private Optional<String> middleName;

// Good - nullable field with annotation
@Nullable
private String middleName;
```

### Use Null Safety Annotations

```java
import org.jspecify.annotations.Nullable;
import org.jspecify.annotations.NonNull;

// Good - explicit null contract
public @NonNull User createUser(@NonNull String name, @Nullable String email) {
    Objects.requireNonNull(name, "name cannot be null");
    return new User(name, email);
}
```

### Defensive Coding with Objects.requireNonNull

```java
public class UserService {
    private final UserRepository repository;
    private final EmailService emailService;

    // Good - fail-fast validation in constructor
    public UserService(UserRepository repository, EmailService emailService) {
        this.repository = Objects.requireNonNull(repository, "repository cannot be null");
        this.emailService = Objects.requireNonNull(emailService, "emailService cannot be null");
    }
}
```

## Null Handling

### Optional Transformation with map/flatMap

```java
// Good - chained transformations
String city = findUserById(id)
    .map(User::getAddress)
    .map(Address::getCity)
    .orElse("Unknown");

// Good - flatMap for Optional-returning methods
Optional<Order> latestOrder = findUserById(id)
    .flatMap(User::getLatestOrder);
```

### Prefer orElseGet for Expensive Defaults

```java
// Good - lazy evaluation for expensive default
User user = findUserById(id)
    .orElseGet(() -> userService.createDefaultUser());

// Bad - always evaluates default
User user = findUserById(id)
    .orElse(userService.createDefaultUser()); // Always creates default user!
```

### Use orElseThrow for Required Values

```java
// Good - explicit exception for missing required value
User user = findUserById(id)
    .orElseThrow(() -> new UserNotFoundException("User not found: " + id));

// Good - Java 10+ simplified version
User user = findUserById(id)
    .orElseThrow(); // Throws NoSuchElementException
```

### Avoid Optional.get() Without Check

```java
// Bad - may throw NoSuchElementException
User user = findUserById(id).get();

// Good - use orElseThrow with meaningful exception
User user = findUserById(id)
    .orElseThrow(() -> new IllegalStateException("Expected user to exist"));

// Good - check presence first if needed
Optional<User> userOpt = findUserById(id);
if (userOpt.isPresent()) {
    User user = userOpt.get();
    // ...
}

// Better - use ifPresent or map
findUserById(id).ifPresent(user -> {
    // Process user
});
```

### Filter with Optional

```java
// Good - combine filter with map
Optional<String> activeUserEmail = findUserById(id)
    .filter(User::isActive)
    .map(User::getEmail);

// Equivalent to
Optional<String> activeUserEmail = findUserById(id)
    .flatMap(user -> user.isActive()
        ? Optional.of(user.getEmail())
        : Optional.empty());
```

### Optional in Streams

```java
// Good - filter out empty Optionals (Java 9+)
List<User> users = userIds.stream()
    .map(this::findUserById)
    .flatMap(Optional::stream)
    .toList();

// Pre-Java 9
List<User> users = userIds.stream()
    .map(this::findUserById)
    .filter(Optional::isPresent)
    .map(Optional::get)
    .collect(Collectors.toList());
```

## Quick Reference: Type Safety Checklist

- [ ] Return `Optional<T>` for potentially absent values
- [ ] Never use `Optional` as method parameter or field
- [ ] Use `@Nullable`/`@NonNull` annotations consistently
- [ ] Validate non-null parameters with `Objects.requireNonNull()`
- [ ] Prefer `orElseGet()` over `orElse()` for expensive defaults
- [ ] Use `orElseThrow()` for required values
- [ ] Never call `Optional.get()` without checking presence
- [ ] Use `map()`/`flatMap()` for Optional transformations
