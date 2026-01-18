---
name: Concurrency
category: Java
tags: [java, concurrency, completablefuture, virtual-threads, async]
activation:
  keywords: [completablefuture, async, virtual, thread, executor, concurrent]
  file_patterns: ["**/*.java"]
---

# Concurrency Pattern

## AI Quick Reference

**Purpose**: Implement safe, efficient concurrent and asynchronous operations in Java.

**Key Rules**:
1. Use `CompletableFuture` for async operations, not raw threads
2. Handle errors with `exceptionally()` or `handle()`
3. Use virtual threads (Java 21) for IO-bound tasks
4. Always shutdown ExecutorService in finally block or try-with-resources
5. Prefer immutable objects and records for thread safety

**Quick Patterns**:

```java
// CompletableFuture with error handling
CompletableFuture<User> userFuture = fetchUserAsync(id)
    .orTimeout(5, TimeUnit.SECONDS)
    .exceptionally(ex -> User.anonymous());

// Virtual threads for IO (Java 21)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<String>> futures = urls.stream()
        .map(url -> executor.submit(() -> fetch(url)))
        .toList();
}

// Parallel execution
CompletableFuture.allOf(userFuture, ordersFuture, prefsFuture)
    .thenApply(v -> new Dashboard(
        userFuture.join(),
        ordersFuture.join(),
        prefsFuture.join()
    ));
```

---

## Human Documentation

### When to Apply

- Making HTTP calls or database queries that shouldn't block
- Processing multiple independent operations in parallel
- Handling high-concurrency workloads (thousands of concurrent tasks)
- Migrating from blocking to non-blocking code

### Implementation Guide

#### 1. CompletableFuture Basics

```java
// Create async operation
CompletableFuture<User> future = CompletableFuture.supplyAsync(() -> {
    return userRepository.findById(id);
});

// Transform result
CompletableFuture<String> emailFuture = future
    .thenApply(User::getEmail)
    .thenApply(String::toLowerCase);

// Consume result
future.thenAccept(user -> log.info("Found: {}", user.getName()));
```

#### 2. Error Handling

```java
// Recover from errors
CompletableFuture<User> userFuture = fetchUserAsync(id)
    .exceptionally(ex -> {
        log.warn("Fetch failed, using default", ex);
        return User.anonymous();
    });

// Handle both success and failure
CompletableFuture<User> userFuture = fetchUserAsync(id)
    .handle((user, ex) -> {
        if (ex != null) {
            metrics.incrementFailure();
            return userCache.get(id);
        }
        metrics.incrementSuccess();
        return user;
    });
```

#### 3. Virtual Threads (Java 21)

Use virtual threads for IO-bound operations that would otherwise block:

```java
// Good - scales to thousands of concurrent tasks
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Response>> responses = requests.stream()
        .map(req -> executor.submit(() -> httpClient.send(req)))
        .toList();

    for (Future<Response> future : responses) {
        processResponse(future.get());
    }
}

// Don't use for CPU-bound work - use ForkJoinPool instead
ForkJoinPool.commonPool().submit(() -> {
    // Heavy computation
});
```

#### 4. Thread-Safe Collections

```java
// Use concurrent collections
private final ConcurrentHashMap<String, User> cache = new ConcurrentHashMap<>();
private final CopyOnWriteArrayList<Listener> listeners = new CopyOnWriteArrayList<>();

// Atomic operations
private final AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();

// Atomic reference for config updates
private final AtomicReference<Config> config = new AtomicReference<>(defaultConfig);
config.updateAndGet(c -> c.withTimeout(newTimeout));
```

### Anti-Patterns

- Using raw `Thread` instead of `ExecutorService` or `CompletableFuture`
- Not shutting down ExecutorService (causes resource leaks)
- Using `synchronized` blocks when concurrent collections would suffice
- Blocking virtual threads with CPU-intensive operations
- Ignoring exceptions in async callbacks

### Migration: Virtual Threads

```java
// Before (platform threads - limited scalability)
ExecutorService executor = Executors.newFixedThreadPool(100);

// After (virtual threads - unlimited scalability for IO)
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

// Code using the executor remains unchanged!
executor.submit(() -> fetchData(url));
```

### Examples

See `SKILL.md` for comprehensive examples and the concurrency section.
