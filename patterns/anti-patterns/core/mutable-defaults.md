---
name: "Mutable Defaults"
severity: "high"
category: "Data Handling"
tags:
  - bugs
  - state
  - functions
detection:
  patterns:
    - "def\\s+\\w+\\s*\\([^)]*=\\s*\\[\\s*\\]"
    - "def\\s+\\w+\\s*\\([^)]*=\\s*\\{\\s*\\}"
    - "def\\s+\\w+\\s*\\([^)]*=\\s*set\\s*\\(\\s*\\)"
    - "function\\s+\\w+\\s*\\([^)]*=\\s*\\[\\s*\\]"
    - "function\\s+\\w+\\s*\\([^)]*=\\s*\\{\\s*\\}"
    - "\\w+\\s*=\\s*\\([^)]*=\\s*\\[\\s*\\]\\s*\\)\\s*=>"
  file_extensions:
    - ".py"
    - ".js"
    - ".ts"
    - ".rb"
  thresholds:
    max_occurrences: 0
version: "1.0"
last_updated: "2026-01-20"
---

# Mutable Defaults

> Using mutable objects (lists, dicts, sets, objects) as default argument values, leading to shared state between function calls.

---

## AI Quick Reference

### Detection Triggers
- Default argument is `[]`, `{}`, `set()`, or any mutable object
- Default argument is a class instance
- Default argument is a mutable data structure
- Same default value shared across calls (bug symptoms)

### Quick Detection Checklist
- [ ] Function parameter defaults to `[]` (empty list)
- [ ] Function parameter defaults to `{}` (empty dict)
- [ ] Function parameter defaults to `set()`
- [ ] Function parameter defaults to a class instance
- [ ] Unexpected data persisting between function calls

### Language-Specific Patterns

| Language | Mutable Default Pattern | Fix Pattern |
|----------|------------------------|-------------|
| Python | `def f(x=[])` | `def f(x=None); x = x or []` |
| Python | `def f(x={})` | `def f(x=None); x = x if x is not None else {}` |
| JavaScript | `function f(x = [])` | Often safe, but watch for mutations |
| Ruby | `def f(x = [])` | Similar to Python |

### Immediate Fix Actions
1. **Change default to None**: Use `None` as the default
2. **Create inside function**: Instantiate the mutable object inside the function body
3. **Use sentinel pattern**: For distinguishing `None` from "not provided"

### Severity Assessment
| Condition | Severity | Action |
|-----------|----------|--------|
| Python mutable default | high | Warn - likely bug |
| JavaScript/TypeScript array default | medium | Info - review for mutations |
| Any mutable default with modification | critical | Block - definite bug |

---

## Problem

### What It Is

In Python (and similar languages), default argument values are evaluated once when the function is defined, not each time it's called. If the default is a mutable object (list, dict, set), the same object is reused across all calls, causing state to persist unexpectedly.

### Why It's Harmful

1. **Silent bugs**: Data accumulates across calls without obvious errors
2. **Non-deterministic**: Function behavior depends on call history
3. **Hard to reproduce**: Bugs only appear after multiple calls
4. **Testing surprises**: Tests may pass individually but fail together
5. **Security risk**: Sensitive data may leak between unrelated calls

### Common Causes

- Not understanding Python's evaluation model for defaults
- Coming from languages where defaults work differently
- Quick prototyping without considering edge cases
- Copy-paste errors from examples that happen to work

---

## Detection

### Signs to Look For

1. **Data accumulation**: Lists growing unexpectedly between calls
2. **Stale data**: Previous call's data appearing in current call
3. **Flaky tests**: Tests passing alone but failing when run together
4. **Memory growth**: Objects not being garbage collected

### Code Examples (Bad)

#### Example 1: Python List Default

```python
def add_item(item, items=[]):
    items.append(item)
    return items

# First call - seems fine
result1 = add_item('a')  # Returns ['a']

# Second call - BUG!
result2 = add_item('b')  # Returns ['a', 'b'] - unexpected!

# Third call
result3 = add_item('c')  # Returns ['a', 'b', 'c'] - getting worse!
```

**Why this is problematic:** The empty list `[]` is created once at function definition. All calls share the same list.

#### Example 2: Python Dict Default

```python
def create_user(name, settings={}):
    settings['name'] = name
    return settings

user1 = create_user('Alice')  # {'name': 'Alice'}
user2 = create_user('Bob')    # {'name': 'Bob'} - But wait...

print(user1)  # {'name': 'Bob'} - Alice's data was overwritten!
print(user1 is user2)  # True - They're the same dict!
```

**Why this is problematic:** Both users share the same settings dict. Modifying one affects the other.

#### Example 3: Class Instance Default

```python
class Config:
    def __init__(self):
        self.options = []

def process(data, config=Config()):
    config.options.append(data)
    return config.options

result1 = process('x')  # ['x']
result2 = process('y')  # ['x', 'y'] - config persists!
```

**Why this is problematic:** The Config instance is created once and reused.

#### Example 4: JavaScript Mutation Issue

```javascript
// JavaScript evaluates defaults per-call, BUT mutation is still dangerous
function addTag(item, tags = []) {
    tags.push(item.tag);  // Mutating the passed-in array
    return tags;
}

const sharedTags = [];
addTag({tag: 'a'}, sharedTags);
addTag({tag: 'b'}, sharedTags);
console.log(sharedTags);  // ['a', 'b'] - caller's array was modified!
```

**Why this is problematic:** While JS creates new defaults, mutating passed arrays affects the caller.

---

## Solution

### Refactoring Steps

1. **Identify mutable defaults**: Search for `=[]`, `={}`, `=set()` in function signatures
2. **Change to None**: Use `None` as the default value
3. **Create inside function**: Instantiate the mutable object in the function body
4. **Document the pattern**: Add a comment explaining the None-check pattern

### Code Examples (Good)

#### Fixed Example 1: None Default Pattern

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Now each call gets its own list
result1 = add_item('a')  # ['a']
result2 = add_item('b')  # ['b'] - Correct!
result3 = add_item('c')  # ['c'] - Correct!

# Can still pass existing list
existing = ['x', 'y']
result4 = add_item('z', existing)  # ['x', 'y', 'z']
```

**Why this is better:** Each call without an argument gets a fresh list.

#### Fixed Example 2: Concise None Check

```python
def create_user(name, settings=None):
    settings = settings if settings is not None else {}
    # Or using walrus operator (Python 3.8+):
    # settings = settings or {}  # Note: falsy values treated as None
    settings['name'] = name
    return settings

user1 = create_user('Alice')  # {'name': 'Alice'}
user2 = create_user('Bob')    # {'name': 'Bob'}

print(user1)  # {'name': 'Alice'} - Correct!
print(user1 is user2)  # False - Different dicts!
```

**Why this is better:** Each user gets their own settings dict.

#### Fixed Example 3: Factory Function

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Config:
    options: List[str] = field(default_factory=list)

def process(data, config=None):
    if config is None:
        config = Config()
    config.options.append(data)
    return config.options

result1 = process('x')  # ['x']
result2 = process('y')  # ['y'] - Fresh config each time!
```

**Why this is better:** Uses `default_factory` for dataclasses, None pattern for function.

#### Fixed Example 4: JavaScript Immutable Approach

```javascript
function addTag(item, tags = []) {
    return [...tags, item.tag];  // Return new array, don't mutate
}

const sharedTags = [];
const result1 = addTag({tag: 'a'}, sharedTags);
const result2 = addTag({tag: 'b'}, sharedTags);

console.log(sharedTags);  // [] - Original unchanged
console.log(result1);     // ['a']
console.log(result2);     // ['b']
```

**Why this is better:** Returns new array instead of mutating, caller's data is safe.

### Prevention Strategies

- Enable linter rules: `pylint` W0102 (dangerous-default-value)
- Code review checklist: "No mutable default arguments"
- Use type hints - they make the issue more visible: `def f(x: List[str] = None)`
- Prefer immutable defaults where possible (strings, numbers, tuples, None)

---

## Exceptions

### When It's Acceptable

1. **Intentional caching**: Function-level memoization using default dict
2. **Configuration singletons**: Explicitly documented shared state
3. **Performance optimization**: Avoiding repeated object creation (with clear documentation)

### How to Document Exceptions

```python
# EXCEPTION: mutable-defaults
# Reason: Intentional memoization cache. The default dict stores
#         previously computed results to avoid redundant calculations.
# Behavior: Cache persists for lifetime of function definition.
# Reviewed: 2026-01-20
def fibonacci(n, _cache={0: 0, 1: 1}):
    if n not in _cache:
        _cache[n] = fibonacci(n-1) + fibonacci(n-2)
    return _cache[n]
```

---

## Related Anti-Patterns

- [God Object](./god-object.md) - May contain methods with mutable defaults
- [Magic Numbers](./magic-numbers.md) - Often seen together with poor defaults

---

## References

- [Python FAQ: Default Parameter Values](https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects)
- [Pylint W0102](https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/dangerous-default-value.html)
- [Effective Python, Item 24](https://effectivepython.com/) - Brett Slatkin
