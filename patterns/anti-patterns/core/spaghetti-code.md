---
name: "Spaghetti Code"
severity: "high"
category: "Control Flow"
tags:
  - complexity
  - maintainability
  - readability
detection:
  patterns:
    - "(if|else|elif|switch|case|while|for|try|catch).*\\{[^}]*(if|else|elif|switch|case|while|for|try|catch)"
    - "goto\\s+"
    - "break\\s+\\w+"
    - "continue\\s+\\w+"
  file_extensions:
    - ".py"
    - ".js"
    - ".ts"
    - ".java"
    - ".go"
    - ".cs"
    - ".c"
    - ".cpp"
    - ".php"
  thresholds:
    max_cyclomatic_complexity: 15
    max_cognitive_complexity: 20
    max_function_length: 50
version: "1.0"
last_updated: "2026-01-20"
---

# Spaghetti Code

> Code with tangled, complex control flow that is difficult to follow, understand, and maintain.

---

## AI Quick Reference

### Detection Triggers
- Cyclomatic complexity > 15 per function
- Cognitive complexity > 20 per function
- Function length > 50 lines
- Multiple exit points (>3 return statements)
- Deeply nested conditionals (>4 levels)
- Use of goto, labeled breaks, or complex continue statements

### Quick Detection Checklist
- [ ] Function has >15 decision points (if/else/switch/loop)
- [ ] Code has >4 levels of nesting
- [ ] Function has >3 return statements
- [ ] Control flow requires tracing multiple branches mentally
- [ ] Presence of goto or labeled jumps

### Complexity Thresholds

| Metric | Acceptable | Warning | Critical |
|--------|------------|---------|----------|
| Cyclomatic Complexity | 1-10 | 11-15 | >15 |
| Cognitive Complexity | 1-15 | 16-20 | >20 |
| Function Length | 1-30 lines | 31-50 lines | >50 lines |
| Nesting Depth | 1-3 | 4 | >4 |

### Immediate Fix Actions
1. **Extract methods**: Break complex functions into smaller, focused functions
2. **Use early returns**: Replace deep nesting with guard clauses
3. **Replace conditionals**: Use polymorphism or strategy pattern for complex branching
4. **Flatten loops**: Extract inner loops into separate functions

### Severity Assessment
| Condition | Severity | Action |
|-----------|----------|--------|
| Cyclomatic >20 OR Nesting >5 | critical | Block - must refactor |
| Cyclomatic >15 OR Nesting >4 | high | Warn - should refactor |
| Cyclomatic >10 | medium | Info - consider refactoring |

---

## Problem

### What It Is

Spaghetti code is a pejorative term for code with a complex, tangled control flow structure. Like a plate of spaghetti where individual strands interweave unpredictably, spaghetti code has execution paths that twist and turn in ways that are difficult to follow.

### Why It's Harmful

1. **Cognitive overload**: Requires holding multiple branches in memory simultaneously
2. **Bug magnet**: Complex paths create hiding spots for bugs
3. **Testing nightmare**: Exponential test cases needed to cover all paths
4. **Modification risk**: Changes in one area unexpectedly affect others
5. **Onboarding barrier**: New developers struggle to understand the logic

### Common Causes

- Incremental feature additions without refactoring
- Copy-paste programming with slight modifications
- Defensive coding taken to extremes (too many edge case checks)
- Lack of design patterns knowledge
- Business logic growing organically without structure
- Legacy code accumulating patches over years

---

## Detection

### Signs to Look For

1. **Arrow code**: Code that forms an arrow shape due to deep nesting
2. **Multiple paths**: Many if/else branches with different outcomes
3. **Loop complexity**: Nested loops with conditional breaks/continues
4. **Exception handling**: Try/catch blocks with complex recovery logic
5. **State machines**: Implicit state machines without clear structure

### Code Examples (Bad)

#### Example 1: Arrow Anti-Pattern

```python
def process_order(order):
    if order:
        if order.is_valid():
            if order.customer:
                if order.customer.is_active():
                    if order.items:
                        if len(order.items) > 0:
                            if order.payment:
                                if order.payment.is_verified():
                                    # Finally do something
                                    return process_payment(order)
                                else:
                                    return "Payment not verified"
                            else:
                                return "No payment method"
                        else:
                            return "No items in order"
                    else:
                        return "Items is None"
                else:
                    return "Customer inactive"
            else:
                return "No customer"
        else:
            return "Invalid order"
    else:
        return "No order"
```

**Why this is problematic:** 8 levels of nesting, difficult to trace which return corresponds to which condition.

#### Example 2: Complex Conditional Logic

```javascript
function calculateDiscount(user, order, coupon) {
    let discount = 0;

    if (user.isPremium) {
        if (order.total > 100) {
            if (coupon && coupon.isValid) {
                if (coupon.type === 'percentage') {
                    discount = order.total * (coupon.value / 100);
                    if (discount > 50) {
                        discount = 50;
                    }
                } else if (coupon.type === 'fixed') {
                    discount = coupon.value;
                    if (discount > order.total) {
                        discount = order.total;
                    }
                }
            } else {
                discount = order.total * 0.1;
            }
        } else {
            if (coupon && coupon.isValid) {
                if (coupon.type === 'percentage') {
                    discount = order.total * (coupon.value / 100);
                } else {
                    discount = coupon.value;
                }
            } else {
                discount = order.total * 0.05;
            }
        }
    } else {
        if (coupon && coupon.isValid) {
            if (order.total > 50) {
                // ... more nested logic
            }
        }
    }

    return discount;
}
```

**Why this is problematic:** Cyclomatic complexity ~15, many branches, duplicate logic patterns.

---

## Solution

### Refactoring Steps

1. **Identify guard clauses**: Find conditions that should exit early
2. **Extract helper functions**: Each logical concern becomes its own function
3. **Use lookup tables**: Replace switch/case with data structures where possible
4. **Apply design patterns**: Strategy, State, or Chain of Responsibility
5. **Flatten step by step**: Reduce one level of nesting at a time

### Code Examples (Good)

#### Fixed Example 1: Guard Clauses

```python
def process_order(order):
    if not order:
        return "No order"

    if not order.is_valid():
        return "Invalid order"

    if not order.customer:
        return "No customer"

    if not order.customer.is_active():
        return "Customer inactive"

    if not order.items or len(order.items) == 0:
        return "No items in order"

    if not order.payment:
        return "No payment method"

    if not order.payment.is_verified():
        return "Payment not verified"

    return process_payment(order)
```

**Why this is better:** Linear flow, each check is independent, easy to add/remove validations.

#### Fixed Example 2: Extracted Functions

```javascript
function calculateDiscount(user, order, coupon) {
    const baseDiscount = getBaseDiscount(user, order);
    const couponDiscount = getCouponDiscount(coupon, order);

    return Math.max(baseDiscount, couponDiscount);
}

function getBaseDiscount(user, order) {
    if (!user.isPremium) {
        return 0;
    }

    const rate = order.total > 100 ? 0.10 : 0.05;
    return order.total * rate;
}

function getCouponDiscount(coupon, order) {
    if (!coupon || !coupon.isValid) {
        return 0;
    }

    const rawDiscount = coupon.type === 'percentage'
        ? order.total * (coupon.value / 100)
        : coupon.value;

    return Math.min(rawDiscount, order.total, 50);
}
```

**Why this is better:** Each function has single responsibility, easy to test individually, readable names explain intent.

### Prevention Strategies

- Set complexity thresholds in linters (ESLint: complexity, max-depth)
- Code review rule: "Can you explain this function in one sentence?"
- Refactor when adding to existing complex functions
- Write tests first - complex code is hard to test

---

## Exceptions

### When It's Acceptable

1. **State machines**: Explicit, well-documented state machines may have inherent complexity
2. **Parsers/compilers**: Parsing logic may require complex branching
3. **Performance-critical code**: Sometimes flat, complex code is faster than function calls
4. **Generated code**: Auto-generated code shouldn't be manually refactored

### How to Document Exceptions

When complex code is intentional:

```python
# EXCEPTION: spaghetti-code
# Reason: This is a state machine implementing protocol X.
#         Complexity is inherent to the specification.
# Complexity: Cyclomatic 18, documented in design doc Y
# Reviewed: 2026-01-20
def protocol_handler(state, input):
    ...
```

---

## Related Anti-Patterns

- [Deep Nesting](./deep-nesting.md) - A specific type of spaghetti code
- [God Object](./god-object.md) - Often contains spaghetti code within

---

## References

- [Cyclomatic Complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity) - McCabe, 1976
- [Cognitive Complexity](https://www.sonarsource.com/resources/white-papers/cognitive-complexity/) - SonarSource
- [Refactoring](https://refactoring.com/) - Martin Fowler
- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/) - Robert C. Martin
