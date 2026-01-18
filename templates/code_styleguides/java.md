# Google Java Style Guide Summary

## AI Quick Reference

### Formatting
- 2-space indentation, no tabs
- Column limit: 100 characters
- One statement per line, braces on same line (`{` at end)
- Braces required for all `if`, `for`, `while`, `do` (even single-line)
- Single blank line between methods and logical sections

### Naming Conventions
- **Classes**: `UpperCamelCase` (nouns: `UserService`, `HttpClient`)
- **Methods**: `lowerCamelCase` (verbs: `sendMessage`, `getUserById`)
- **Constants**: `UPPER_SNAKE_CASE` (`MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`)
- **Variables/Parameters**: `lowerCamelCase` (never single letter except loops)
- **Packages**: all lowercase, no underscores (`com.example.myapp`)

### Type Patterns
- Prefer `Optional<T>` for nullable return values
- Use `var` for local variables with obvious types (Java 10+)
- Prefer interfaces over implementation types (`List<>` not `ArrayList<>`)
- Use records for immutable data carriers (Java 17+)

### Avoid
- Wildcard imports (`import java.util.*`)
- Unused imports (remove them)
- `Optional` as parameter or field type
- Raw generic types (`List` instead of `List<String>`)
- Mutable static fields (use constants or dependency injection)

---

This document summarizes key rules and best practices from the Google Java Style Guide.

## 1. Source File Structure

### File Organization
1. License/copyright information (if any)
2. Package statement
3. Import statements
4. Exactly one top-level class

### Import Statements
- **No wildcard imports.** Always import specific classes.
- **No unused imports.** Remove them.
- **Order:** Static imports first, then non-static. Within each block, alphabetical order.
- **No line-wrapping** for import statements.

```java
// Good
import java.util.List;
import java.util.Map;

// Bad
import java.util.*;
```

## 2. Formatting

### Braces
- **Always use braces** for `if`, `else`, `for`, `do`, and `while`, even when the body is empty or contains only a single statement.
- **K&R style:** Opening brace at end of line, closing brace on its own line.

```java
// Good
if (condition) {
    doSomething();
}

// Bad - missing braces
if (condition)
    doSomething();
```

### Indentation
- **2 spaces** for indentation. No tabs.
- **4 spaces** for continuation lines.

### Line Length
- **100 characters maximum** per line.
- Break long lines at operators, after commas, or before method chains.

### Whitespace
- One blank line between methods.
- No trailing whitespace.
- Space after keywords (`if`, `for`, `while`, `catch`).
- Space around binary operators (`+`, `-`, `=`, `==`).

## 3. Naming

### Package Names
- All lowercase, no underscores.
- Reverse domain name notation: `com.example.projectname`

### Class Names
- **UpperCamelCase**
- Nouns or noun phrases: `UserService`, `HttpClient`, `OrderValidator`
- Test classes: name of class being tested + `Test` (e.g., `UserServiceTest`)

### Method Names
- **lowerCamelCase**
- Verbs or verb phrases: `sendMessage()`, `getUserById()`, `isValid()`
- Boolean methods: prefer `is`, `has`, `can` prefixes

### Constant Names
- **UPPER_SNAKE_CASE**
- For `static final` fields with immutable values.

```java
public static final int MAX_RETRY_COUNT = 3;
public static final Duration DEFAULT_TIMEOUT = Duration.ofSeconds(30);
```

### Variable and Parameter Names
- **lowerCamelCase**
- Descriptive names, not single letters (except `i`, `j`, `k` for loop indices).
- No Hungarian notation (`strName`, `iCount`).

```java
// Good
int retryCount = 0;
String userName = "John";

// Bad
int n = 0;
String strName = "John";
```

## 4. Programming Practices

### `@Override`
- Always use `@Override` when overriding a method.

### Exception Handling
- Never ignore caught exceptions silently.
- At minimum, log the exception or add a comment explaining why it's ignored.

```java
// Bad
try {
    doSomething();
} catch (Exception e) {
    // Empty - bad!
}

// Good
try {
    doSomething();
} catch (Exception e) {
    log.warn("Expected failure during shutdown", e);
}
```

### Static Members
- Access static members using the class name, not an instance.

```java
// Good
Foo.staticMethod();

// Bad
foo.staticMethod();
```

### Finalizers
- **Never override `finalize()`.** Use `try-with-resources` or `Cleaner` instead.

## 5. Javadoc

### When Required
- Every public class and public/protected member.
- Exception: "simple, obvious" methods like getters.

### Format
```java
/**
 * Brief summary ending with a period.
 *
 * <p>Additional paragraphs with more detail.
 *
 * @param name description
 * @return description
 * @throws ExceptionType description
 */
public String process(String name) throws ProcessingException {
    // ...
}
```

### Rules
- First sentence is a summary fragment (not a complete sentence structure required).
- Use `@param`, `@return`, `@throws` tags in that order.
- No blank line between the description and tag block.

## 6. Modern Java Features (Java 17+)

### Records
- Use for immutable data carriers instead of manual POJO classes.

```java
// Good - concise and immutable
public record User(String id, String name, String email) {}

// Instead of verbose class with equals/hashCode/toString
```

### Sealed Classes
- Use to restrict inheritance hierarchies.

```java
public sealed interface Result<T> permits Success, Failure {}
public record Success<T>(T value) implements Result<T> {}
public record Failure<T>(String error) implements Result<T> {}
```

### Pattern Matching
- Use pattern matching for instanceof (Java 17+).

```java
// Good
if (obj instanceof String s) {
    return s.length();
}

// Bad - redundant cast
if (obj instanceof String) {
    String s = (String) obj;
    return s.length();
}
```

### Switch Expressions
- Prefer switch expressions over switch statements.

```java
// Good
String result = switch (day) {
    case MONDAY, FRIDAY -> "Work";
    case SATURDAY, SUNDAY -> "Rest";
    default -> "Unknown";
};
```

### Local Variable Type Inference
- Use `var` when the type is obvious from context.

```java
// Good - type is obvious
var users = new ArrayList<User>();
var response = httpClient.send(request);

// Bad - type not obvious
var result = process(data);  // What type is result?
```

## 7. Common Anti-Patterns

### Avoid
- **God classes**: Classes with too many responsibilities
- **Magic numbers**: Use named constants instead
- **Deep nesting**: Refactor to reduce indentation levels
- **Long methods**: Break into smaller, focused methods
- **Mutable shared state**: Prefer immutability and local state

### Prefer
- **Composition over inheritance**
- **Dependency injection over static factories**
- **Immutable objects** (records, final fields)
- **Early returns** to reduce nesting
- **Small, focused methods** (< 20 lines ideal)

*Source: [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)*
