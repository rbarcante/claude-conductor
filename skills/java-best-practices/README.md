# Java Best Practices Skill

A Conductor skill providing guidance for writing type-safe, concurrent, and modern Java code targeting Java 17+ and Java 21 LTS.

## Overview

This skill activates when working with Java files and provides guidance on:

- **Type Safety**: Optional usage, @Nullable/@NonNull annotations, defensive coding patterns
- **Concurrency**: CompletableFuture, virtual threads (Java 21), ExecutorService, thread safety
- **Modern Features**: Records, sealed classes, pattern matching, switch expressions

## Target Versions

- **Java 17 LTS**: Records, sealed classes, pattern matching for instanceof
- **Java 21 LTS**: Virtual threads, pattern matching in switch, sequenced collections

## Activation

The skill automatically activates when:

- Working with `.java` files
- Working with `pom.xml` or `build.gradle` files
- Task description contains keywords: `java`, `optional`, `completablefuture`, `record`, `sealed`, `virtual thread`
- Project tech stack includes Java

## Patterns Provided

| Pattern | Description |
|---------|-------------|
| [type-safety](patterns/type-safety.md) | Optional best practices, null safety annotations, defensive coding |
| [concurrency](patterns/concurrency.md) | CompletableFuture, virtual threads, thread-safe patterns |
| [modern-features](patterns/modern-features.md) | Records, sealed classes, pattern matching |

## Usage Examples

### Type-Safe Optional Handling

```java
// Good - explicit Optional handling
public Optional<User> findUserById(String id) {
    return Optional.ofNullable(userRepository.findById(id));
}

// Usage with map/flatMap
String userName = findUserById("123")
    .map(User::getName)
    .orElse("Unknown");
```

### Modern Records

```java
// Immutable data carrier with automatic equals, hashCode, toString
public record User(String id, String name, String email) {
    // Compact constructor for validation
    public User {
        Objects.requireNonNull(id, "id cannot be null");
        Objects.requireNonNull(name, "name cannot be null");
    }
}
```

### Virtual Threads (Java 21)

```java
// Lightweight threads for IO-bound operations
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<String>> futures = urls.stream()
        .map(url -> executor.submit(() -> fetchUrl(url)))
        .toList();

    for (Future<String> future : futures) {
        System.out.println(future.get());
    }
}
```

## Related Skills

- **testing-strategies**: For Java testing patterns with JUnit 5
- **api-design**: For REST API development with Spring Boot or Jakarta EE

## Changelog

### 1.0.0

- Initial release
- Type safety patterns with Optional and null annotations
- Concurrency patterns with CompletableFuture and virtual threads
- Modern Java features (records, sealed classes, pattern matching)
