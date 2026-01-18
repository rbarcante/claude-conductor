---
name: Modern Features
category: Java
tags: [java, records, sealed-classes, pattern-matching, switch-expressions]
activation:
  keywords: [record, sealed, permits, instanceof, switch, pattern]
  file_patterns: ["**/*.java"]
---

# Modern Features Pattern

## AI Quick Reference

**Purpose**: Leverage modern Java features (17+, 21+) for cleaner, safer code.

**Key Rules**:
1. Use records for immutable data carriers (DTOs, value objects)
2. Use sealed classes to restrict type hierarchies
3. Use pattern matching with instanceof to avoid explicit casts
4. Use switch expressions instead of switch statements
5. Combine sealed types with pattern matching for exhaustive handling

**Quick Patterns**:

```java
// Record with validation
public record User(String id, String name) {
    public User {
        Objects.requireNonNull(id, "id cannot be null");
    }
}

// Sealed type hierarchy
public sealed interface Shape permits Circle, Rectangle {}
public record Circle(double radius) implements Shape {}
public record Rectangle(double w, double h) implements Shape {}

// Exhaustive pattern matching (Java 21)
double area = switch (shape) {
    case Circle c -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.w() * r.h();
};
```

---

## Human Documentation

### When to Apply

- Creating immutable data transfer objects
- Modeling domain entities with value semantics
- Designing restricted type hierarchies (state machines, result types)
- Replacing instanceof + cast patterns
- Converting switch statements to expressions

### Implementation Guide

#### 1. Records

Records provide immutable data carriers with automatic `equals()`, `hashCode()`, and `toString()`:

```java
// Basic record
public record Point(int x, int y) {}

// Record with compact constructor validation
public record Email(String value) {
    public Email {
        if (value == null || !value.contains("@")) {
            throw new IllegalArgumentException("Invalid email: " + value);
        }
    }
}

// Record with computed properties
public record Rectangle(double width, double height) {
    public double area() {
        return width * height;
    }

    public double perimeter() {
        return 2 * (width + height);
    }
}
```

**Best use cases for records:**
- DTOs (Data Transfer Objects)
- Value objects (Money, Email, Address)
- API responses
- Compound map keys
- Configuration objects

#### 2. Sealed Classes

Sealed classes restrict which classes can extend them:

```java
// Define permitted subtypes
public sealed interface Result<T> permits Success, Failure {}
public record Success<T>(T value) implements Result<T> {}
public record Failure<T>(String error) implements Result<T> {}

// Use with pattern matching for exhaustive handling
public <T> T unwrap(Result<T> result) {
    return switch (result) {
        case Success<T> s -> s.value();
        case Failure<T> f -> throw new RuntimeException(f.error());
    };
}
```

#### 3. Pattern Matching for instanceof

```java
// Before (Java 16-)
if (obj instanceof String) {
    String s = (String) obj;
    return s.length();
}

// After (Java 17+)
if (obj instanceof String s) {
    return s.length();
}

// With guards
if (obj instanceof String s && s.length() > 10) {
    return s.substring(0, 10) + "...";
}
```

#### 4. Switch Expressions (Java 17+)

```java
// Expression form returns a value
String dayType = switch (day) {
    case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "Weekday";
    case SATURDAY, SUNDAY -> "Weekend";
};

// Use yield for complex cases
int score = switch (grade) {
    case "A" -> 4;
    case "B" -> 3;
    case "C" -> 2;
    default -> {
        log.warn("Unknown grade: {}", grade);
        yield 0;
    }
};
```

#### 5. Pattern Matching in Switch (Java 21+)

```java
// Type patterns
String describe(Object obj) {
    return switch (obj) {
        case Integer i -> "Integer: " + i;
        case String s -> "String of length " + s.length();
        case List<?> list -> "List with " + list.size() + " elements";
        case null -> "null";
        default -> "Unknown: " + obj.getClass().getName();
    };
}

// Guards with when
String categorize(Shape shape) {
    return switch (shape) {
        case Circle c when c.radius() > 100 -> "Large circle";
        case Circle c -> "Small circle";
        case Rectangle r when r.width() == r.height() -> "Square";
        case Rectangle r -> "Rectangle";
    };
}
```

### Anti-Patterns

- Using records when you need mutable state
- Using records when you need inheritance
- Not leveraging exhaustive pattern matching with sealed types
- Using `default` in switch when all cases should be explicit
- Forgetting to handle `null` in pattern matching switch

### Examples

See `SKILL.md` for comprehensive examples and the modern features section.
