---
name: "Magic Numbers"
severity: "medium"
category: "Naming"
tags:
  - readability
  - maintainability
  - constants
detection:
  patterns:
    - "(?<!const\\s)(?<!final\\s)(?<!#define\\s)\\b\\d{2,}\\b(?!\\s*[;,\\)]\\s*(//|/\\*|#).*constant)"
    - "\\[\\d+\\]"
    - "==\\s*\\d+|!=\\s*\\d+|>\\s*\\d+|<\\s*\\d+"
  file_extensions:
    - ".py"
    - ".js"
    - ".ts"
    - ".java"
    - ".go"
    - ".cs"
    - ".c"
    - ".cpp"
  thresholds:
    max_magic_numbers_per_file: 5
version: "1.0"
last_updated: "2026-01-20"
---

# Magic Numbers

> Unexplained numeric literals scattered throughout code that lack context about their meaning or purpose.

---

## AI Quick Reference

### Detection Triggers
- Numeric literals (other than 0, 1, -1) used directly in code
- Numbers in array indices, comparisons, or calculations without explanation
- Same number appearing multiple times in different locations
- Numbers in conditionals: `if (status == 3)`

### Quick Detection Checklist
- [ ] Numbers other than 0, 1, -1 used directly in logic
- [ ] Same number repeated in multiple places
- [ ] Numbers in comparisons without named constants
- [ ] Array indices with hardcoded numbers

### Common Magic Numbers to Watch

| Number | Likely Meaning | Better Name |
|--------|---------------|-------------|
| 60 | Seconds/minutes | `SECONDS_PER_MINUTE` |
| 24 | Hours per day | `HOURS_PER_DAY` |
| 1000 | Milliseconds | `MS_PER_SECOND` |
| 86400 | Seconds per day | `SECONDS_PER_DAY` |
| 100 | Percentage base | `PERCENTAGE_BASE` |
| 255 | Max byte value | `MAX_BYTE_VALUE` |

### Immediate Fix Actions
1. **Identify the meaning**: Determine what the number represents
2. **Name it**: Create a descriptive constant name
3. **Declare it**: Add constant at appropriate scope (file, class, module)
4. **Replace all occurrences**: Use find/replace to update all uses

### Severity Assessment
| Condition | Severity | Action |
|-----------|----------|--------|
| >10 magic numbers in file | high | Warn - should fix |
| 5-10 magic numbers | medium | Info - consider fixing |
| <5 magic numbers | low | Note for review |

---

## Problem

### What It Is

Magic numbers are numeric literals that appear in code without explanation. The term "magic" refers to the mysterious nature of these numbers - their meaning is not immediately apparent to readers.

### Why It's Harmful

1. **Poor readability**: `if (retries > 3)` - Why 3? What's special about 3?
2. **Maintenance nightmare**: Changing a value requires finding all occurrences
3. **Bug-prone**: Easy to change one occurrence and miss others
4. **No domain context**: Numbers don't convey business meaning
5. **Testing difficulty**: Hard to test boundary conditions without understanding limits

### Common Causes

- Quick prototyping that never gets cleaned up
- Copy-pasting code with embedded constants
- Lack of awareness that numbers need explanation
- "I'll remember what this means" mentality
- Time pressure during development

---

## Detection

### Signs to Look For

1. **Numeric comparisons**: `if (age >= 18)`, `if (count > 100)`
2. **Array sizing**: `new int[256]`, `buffer = [0] * 1024`
3. **Loop bounds**: `for (i = 0; i < 52; i++)`
4. **Calculations**: `total * 0.0825`, `price * 1.15`
5. **Status codes**: `if (response.status == 404)`

### Code Examples (Bad)

#### Example 1: Multiple Magic Numbers

```python
def calculate_shipping(weight, distance):
    if weight > 50:
        base_cost = 25.99
    else:
        base_cost = 12.99

    if distance > 500:
        multiplier = 1.5
    elif distance > 100:
        multiplier = 1.2
    else:
        multiplier = 1.0

    return base_cost * multiplier * 1.0825  # What is 1.0825?
```

**Why this is problematic:** What do 50, 500, 100 represent? What is 1.0825? None of these numbers have context.

#### Example 2: Scattered Magic Numbers

```javascript
function processUser(user) {
    if (user.age < 13) {
        return 'child';
    } else if (user.age < 18) {
        return 'minor';
    } else if (user.age >= 65) {
        return 'senior';
    }

    if (user.posts > 1000) {
        user.badge = 'power_user';
    } else if (user.posts > 100) {
        user.badge = 'active';
    }

    // Later in code...
    if (user.loginAttempts > 5) {
        lockAccount(user, 30 * 60 * 1000); // What is this calculation?
    }
}
```

**Why this is problematic:** Age thresholds, post counts, login limits, and time calculations are all unexplained.

### Exclusions (Not Magic Numbers)

These are generally acceptable without named constants:
- `0` - Empty, none, start index
- `1` - Single item, increment
- `-1` - Not found, decrement
- `2` - Binary operations, halving
- `100` - When obviously percentage-related in context

---

## Solution

### Refactoring Steps

1. **Survey the codebase**: Find all numeric literals
2. **Group by meaning**: Identify which numbers represent the same concept
3. **Define constants**: Create well-named constants at appropriate scope
4. **Document units**: Include units in names where applicable (MS, SECONDS, BYTES)
5. **Replace and verify**: Replace all occurrences and run tests

### Code Examples (Good)

#### Fixed Example 1: Named Constants

```python
# Shipping configuration
HEAVY_PACKAGE_THRESHOLD_LBS = 50
HEAVY_PACKAGE_BASE_COST = 25.99
STANDARD_PACKAGE_BASE_COST = 12.99

LONG_DISTANCE_THRESHOLD_MILES = 500
MEDIUM_DISTANCE_THRESHOLD_MILES = 100
LONG_DISTANCE_MULTIPLIER = 1.5
MEDIUM_DISTANCE_MULTIPLIER = 1.2

TAX_RATE = 0.0825  # 8.25% sales tax

def calculate_shipping(weight, distance):
    if weight > HEAVY_PACKAGE_THRESHOLD_LBS:
        base_cost = HEAVY_PACKAGE_BASE_COST
    else:
        base_cost = STANDARD_PACKAGE_BASE_COST

    if distance > LONG_DISTANCE_THRESHOLD_MILES:
        multiplier = LONG_DISTANCE_MULTIPLIER
    elif distance > MEDIUM_DISTANCE_THRESHOLD_MILES:
        multiplier = MEDIUM_DISTANCE_MULTIPLIER
    else:
        multiplier = 1.0

    return base_cost * multiplier * (1 + TAX_RATE)
```

**Why this is better:** Every number has a name that explains its purpose. Changes are centralized.

#### Fixed Example 2: Constants with Context

```javascript
const AGE_THRESHOLDS = {
    CHILD_MAX: 12,
    MINOR_MAX: 17,
    SENIOR_MIN: 65
};

const USER_BADGES = {
    POWER_USER_POST_MIN: 1000,
    ACTIVE_USER_POST_MIN: 100
};

const SECURITY = {
    MAX_LOGIN_ATTEMPTS: 5,
    LOCKOUT_DURATION_MS: 30 * 60 * 1000  // 30 minutes
};

function processUser(user) {
    if (user.age <= AGE_THRESHOLDS.CHILD_MAX) {
        return 'child';
    } else if (user.age <= AGE_THRESHOLDS.MINOR_MAX) {
        return 'minor';
    } else if (user.age >= AGE_THRESHOLDS.SENIOR_MIN) {
        return 'senior';
    }

    if (user.posts >= USER_BADGES.POWER_USER_POST_MIN) {
        user.badge = 'power_user';
    } else if (user.posts >= USER_BADGES.ACTIVE_USER_POST_MIN) {
        user.badge = 'active';
    }

    if (user.loginAttempts > SECURITY.MAX_LOGIN_ATTEMPTS) {
        lockAccount(user, SECURITY.LOCKOUT_DURATION_MS);
    }
}
```

**Why this is better:** Constants are grouped by domain, documented with comments where helpful, and easy to modify.

### Prevention Strategies

- Configure linter rules to flag numeric literals (ESLint: no-magic-numbers)
- Code review checklist: "Are all numbers explained?"
- Create a constants file/module early in project setup
- Document the meaning of constants, not just their value

---

## Exceptions

### When It's Acceptable

1. **Obvious mathematical constants**: Using `2` for halving, `360` for degrees
2. **Well-established conventions**: HTTP status codes (200, 404, 500) when context is clear
3. **Array initialization**: `new Array(0)` or obvious sizes
4. **Test data**: Magic numbers in test files for specific test cases (but document why)

### How to Document Exceptions

When a magic number is intentional, document it inline:

```python
# EXCEPTION: magic-number
# Reason: HTTP 404 is a universal standard; naming it would reduce clarity
# Reviewed: 2026-01-20
if response.status_code == 404:
    return None
```

Or use inline comments for truly obvious cases:

```javascript
const half = total / 2;  // Dividing by 2 is self-explanatory
```

---

## Related Anti-Patterns

- [God Object](./god-object.md) - Often contains many magic numbers
- [Spaghetti Code](./spaghetti-code.md) - Magic numbers increase complexity

---

## References

- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/) - Robert C. Martin, Chapter 17
- [ESLint no-magic-numbers rule](https://eslint.org/docs/rules/no-magic-numbers)
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/) - Hunt & Thomas
