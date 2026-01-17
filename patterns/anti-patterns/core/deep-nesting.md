---
name: "Deep Nesting"
severity: "medium"
category: "Control Flow"
tags:
  - readability
  - complexity
  - maintainability
detection:
  patterns:
    - "^(\\s{4}|\\t){4,}"
    - "(if|for|while|switch|try).*\\{[^}]*(if|for|while|switch|try).*\\{[^}]*(if|for|while|switch|try).*\\{[^}]*(if|for|while|switch|try)"
  file_extensions:
    - ".py"
    - ".js"
    - ".ts"
    - ".java"
    - ".go"
    - ".cs"
    - ".c"
    - ".cpp"
    - ".rb"
    - ".php"
  thresholds:
    max_nesting: 4
version: "1.0"
last_updated: "2026-01-20"
---

# Deep Nesting

> Code with excessive levels of indentation from nested control structures, making it hard to follow the logic.

---

## AI Quick Reference

### Detection Triggers
- Nesting depth exceeds 4 levels
- Indentation goes beyond 4 tabs/16 spaces
- Code forms an "arrow" shape pointing right
- Multiple nested loops or conditionals

### Quick Detection Checklist
- [ ] Code indented >4 levels deep
- [ ] Must scroll horizontally to read code
- [ ] Closing braces stack up at the end
- [ ] Difficulty tracking which `}` matches which `{`

### Nesting Thresholds

| Depth | Status | Action |
|-------|--------|--------|
| 1-2 | Good | Normal, maintainable |
| 3 | Acceptable | Watch for growth |
| 4 | Warning | Consider refactoring |
| 5+ | Critical | Must refactor |

### Immediate Fix Actions
1. **Use guard clauses**: Invert conditions and return early
2. **Extract functions**: Each nesting level becomes a function call
3. **Use early returns**: Exit loops with `return` instead of flags
4. **Flatten with &&/||**: Combine simple conditions

### Severity Assessment
| Condition | Severity | Action |
|-----------|----------|--------|
| Nesting depth >5 | high | Warn - should refactor |
| Nesting depth >4 | medium | Info - consider refactoring |
| Nesting depth 4 | low | Note for review |

---

## Problem

### What It Is

Deep nesting occurs when code contains multiple levels of nested control structures (if statements, loops, try/catch blocks). Each level increases the indentation, eventually creating code that is difficult to read and understand.

### Why It's Harmful

1. **Hard to read**: Eyes must track horizontally across the screen
2. **Cognitive load**: Must remember context from multiple levels above
3. **Error-prone**: Easy to put code at wrong nesting level
4. **Testing difficulty**: Each level multiplies possible execution paths
5. **Merge conflicts**: Indentation changes affect entire blocks

### Common Causes

- Adding one more condition to already-nested code
- Fear of creating new functions ("it's just a small addition")
- Defensive programming with many null checks
- Complex business rules expressed directly in code
- Loop-within-loop-within-loop data processing

---

## Detection

### Signs to Look For

1. **Arrow shape**: Code forms `>` pointing right then `<` at the end
2. **Horizontal scroll**: Must scroll right to see all code
3. **Brace stacking**: `}}}}` at the end of functions
4. **Lost context**: Can't tell what level you're in without counting
5. **Long conditions**: Many `&&` or `||` at deep levels

### Code Examples (Bad)

#### Example 1: Classic Arrow Anti-Pattern

```python
def process_data(data):
    if data is not None:
        if len(data) > 0:
            for item in data:
                if item.is_valid():
                    if item.category == 'important':
                        for sub_item in item.children:
                            if sub_item.status == 'active':
                                if sub_item.value > 0:
                                    # Finally, the actual logic
                                    process_item(sub_item)
```

**Why this is problematic:** 8 levels of nesting. The actual logic is buried deep inside multiple conditions.

#### Example 2: Nested Loops with Conditions

```javascript
function findMatches(users, products, orders) {
    const results = [];

    for (const user of users) {
        if (user.isActive) {
            for (const product of products) {
                if (product.inStock) {
                    for (const order of orders) {
                        if (order.userId === user.id) {
                            if (order.productId === product.id) {
                                if (order.status === 'pending') {
                                    results.push({
                                        user: user.name,
                                        product: product.name,
                                        order: order.id
                                    });
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return results;
}
```

**Why this is problematic:** Triple nested loop with conditions creates O(n³) complexity and 6 levels of nesting.

#### Example 3: Try-Catch Nesting

```java
public void processFile(String path) {
    try {
        File file = new File(path);
        if (file.exists()) {
            try {
                BufferedReader reader = new BufferedReader(new FileReader(file));
                try {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        if (line.length() > 0) {
                            try {
                                processLine(line);
                            } catch (ProcessingException e) {
                                // Handle processing error
                            }
                        }
                    }
                } finally {
                    reader.close();
                }
            } catch (FileNotFoundException e) {
                // Handle not found
            }
        }
    } catch (IOException e) {
        // Handle IO error
    }
}
```

**Why this is problematic:** Nested try-catch creates confusing error handling with unclear which catch handles what.

---

## Solution

### Refactoring Steps

1. **Identify the deepest logic**: Find what the code actually does at the innermost level
2. **Invert conditions**: Change `if (x) { ... }` to `if (!x) return;`
3. **Extract inner loops**: Each loop becomes its own function
4. **Combine checks**: Merge related conditions before the main logic
5. **Use early exits**: Return, continue, or break as soon as possible

### Code Examples (Good)

#### Fixed Example 1: Guard Clauses

```python
def process_data(data):
    if data is None or len(data) == 0:
        return

    for item in data:
        process_valid_item(item)


def process_valid_item(item):
    if not item.is_valid():
        return

    if item.category != 'important':
        return

    for sub_item in item.children:
        process_active_sub_item(sub_item)


def process_active_sub_item(sub_item):
    if sub_item.status != 'active':
        return

    if sub_item.value <= 0:
        return

    process_item(sub_item)
```

**Why this is better:** Maximum 2 levels of nesting. Each function has single responsibility.

#### Fixed Example 2: Functional Approach

```javascript
function findMatches(users, products, orders) {
    const activeUsers = users.filter(u => u.isActive);
    const inStockProducts = products.filter(p => p.inStock);
    const pendingOrders = orders.filter(o => o.status === 'pending');

    return pendingOrders
        .filter(order => {
            const user = activeUsers.find(u => u.id === order.userId);
            const product = inStockProducts.find(p => p.id === order.productId);
            return user && product;
        })
        .map(order => ({
            user: activeUsers.find(u => u.id === order.userId).name,
            product: inStockProducts.find(p => p.id === order.productId).name,
            order: order.id
        }));
}
```

**Why this is better:** Declarative style, no nesting, easy to understand intent.

#### Fixed Example 3: Try-with-Resources

```java
public void processFile(String path) {
    Path filePath = Paths.get(path);

    if (!Files.exists(filePath)) {
        return;
    }

    try (BufferedReader reader = Files.newBufferedReader(filePath)) {
        reader.lines()
            .filter(line -> !line.isEmpty())
            .forEach(this::safeProcessLine);
    } catch (IOException e) {
        handleIOError(e);
    }
}

private void safeProcessLine(String line) {
    try {
        processLine(line);
    } catch (ProcessingException e) {
        handleProcessingError(e, line);
    }
}
```

**Why this is better:** Uses try-with-resources, separates error handling, maximum 1 level of nesting.

### Prevention Strategies

- Configure linters to warn on nesting depth (ESLint: max-depth)
- Code review guideline: "No more than 3 levels of nesting"
- When about to add a fourth level, stop and refactor first
- Extract method as soon as you see arrow code forming

---

## Exceptions

### When It's Acceptable

1. **Matrix operations**: Double-nested loops for 2D arrays are sometimes necessary
2. **Tree traversal**: Recursive structures may require depth
3. **Parser implementations**: Complex grammar rules may need nesting
4. **Generated code**: Auto-generated code shouldn't be manually refactored

### How to Document Exceptions

```python
# EXCEPTION: deep-nesting
# Reason: Matrix convolution requires nested iteration over kernel and image.
#         Refactoring would obscure the algorithm's mathematical structure.
# Max Depth: 4 levels
# Reviewed: 2026-01-20
def convolve_2d(image, kernel):
    for i in range(height):
        for j in range(width):
            for ki in range(kernel_height):
                for kj in range(kernel_width):
                    # Convolution calculation
                    ...
```

---

## Related Anti-Patterns

- [Spaghetti Code](./spaghetti-code.md) - Deep nesting is a symptom
- [God Object](./god-object.md) - Large classes often have deeply nested methods

---

## References

- [Flattening Arrow Code](https://blog.codinghorror.com/flattening-arrow-code/) - Jeff Atwood
- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/) - Robert C. Martin, Chapter 3
- [ESLint max-depth rule](https://eslint.org/docs/rules/max-depth)
