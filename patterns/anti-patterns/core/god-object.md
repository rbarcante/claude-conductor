---
name: "God Object"
severity: "high"
category: "Code Structure"
tags:
  - maintainability
  - single-responsibility
  - refactoring
detection:
  patterns:
    - "class\\s+\\w+[^}]{15000,}"
    - "^(def|function|func|public|private|protected)\\s+\\w+.*$"
  file_extensions:
    - ".py"
    - ".js"
    - ".ts"
    - ".java"
    - ".go"
    - ".cs"
    - ".rb"
  thresholds:
    max_lines: 500
    max_methods: 20
    max_dependencies: 15
version: "1.0"
last_updated: "2026-01-20"
---

# God Object

> A class or module that knows too much or does too much, violating the Single Responsibility Principle.

---

## AI Quick Reference

### Detection Triggers
- Class/file exceeds 500 lines of code
- Class has more than 20 methods/functions
- Class has more than 15 dependencies/imports
- Class name contains generic terms: Manager, Handler, Processor, Controller, Service (combined with large size)

### Quick Detection Checklist
- [ ] File line count > 500
- [ ] Method/function count > 20
- [ ] Import/dependency count > 15
- [ ] Multiple unrelated responsibilities in same class

### Metrics Thresholds

| Metric | Warning (High) | Critical |
|--------|----------------|----------|
| Lines of Code | > 500 | > 1000 |
| Methods/Functions | > 20 | > 40 |
| Dependencies | > 15 | > 25 |

### Immediate Fix Actions
1. **Identify responsibilities**: List all distinct responsibilities the class handles
2. **Group related methods**: Cluster methods by their primary concern
3. **Extract classes**: Create new classes for each responsibility cluster
4. **Use composition**: Replace inheritance with composition where appropriate

### Severity Assessment
| Condition | Severity | Action |
|-----------|----------|--------|
| >1000 lines OR >40 methods | critical | Block - must refactor |
| >500 lines OR >20 methods | high | Warn - should refactor |
| >300 lines OR >15 methods | medium | Info - consider refactoring |

---

## Problem

### What It Is

A God Object (also known as "Blob" or "Monster Class") is a class that has grown to handle too many responsibilities. It becomes the central point of the application where most logic resides, making it difficult to understand, test, and maintain.

### Why It's Harmful

1. **Difficult to understand**: New developers struggle to grasp what the class does
2. **Hard to test**: Testing requires extensive mocking and setup
3. **Merge conflicts**: Multiple developers often need to modify the same file
4. **Rigid design**: Changes in one area risk breaking unrelated functionality
5. **Poor reusability**: Cannot reuse individual pieces of functionality

### Common Causes

- Organic growth without refactoring ("just add it here for now")
- Fear of creating new files/classes
- Lack of clear architectural guidelines
- Time pressure leading to shortcuts
- Misunderstanding of the Single Responsibility Principle

---

## Detection

### Signs to Look For

1. **File size**: Scrolling extensively to find methods
2. **Generic naming**: Classes named `ApplicationManager`, `MainController`, `Utils`
3. **Many imports**: Long list of dependencies at the top
4. **Unrelated methods**: Methods that don't logically belong together
5. **Frequent modifications**: File appears in most commits

### Code Examples (Bad)

#### Example 1: Python God Object

```python
class ApplicationManager:
    def __init__(self):
        self.db = Database()
        self.cache = Cache()
        self.email = EmailService()
        self.payment = PaymentProcessor()
        self.auth = AuthService()
        self.logger = Logger()
        # ... 20+ more dependencies

    def create_user(self, data): ...
    def delete_user(self, id): ...
    def send_welcome_email(self, user): ...
    def process_payment(self, order): ...
    def validate_credit_card(self, card): ...
    def generate_report(self, type): ...
    def export_to_csv(self, data): ...
    def import_from_csv(self, file): ...
    def authenticate_user(self, creds): ...
    def refresh_token(self, token): ...
    # ... 50+ more methods handling unrelated concerns
```

**Why this is problematic:** This class handles user management, email, payments, reporting, file I/O, and authentication - at least 6 different responsibilities.

#### Example 2: JavaScript God Object

```javascript
class AppController {
    constructor() {
        this.users = [];
        this.products = [];
        this.orders = [];
        this.settings = {};
        // 500+ lines of initialization
    }

    // User methods (lines 50-200)
    createUser() { /* ... */ }
    updateUser() { /* ... */ }

    // Product methods (lines 201-400)
    addProduct() { /* ... */ }
    removeProduct() { /* ... */ }

    // Order methods (lines 401-600)
    placeOrder() { /* ... */ }
    cancelOrder() { /* ... */ }

    // ... continues for 2000+ lines
}
```

**Why this is problematic:** Single file contains entire application logic with no separation of concerns.

---

## Solution

### Refactoring Steps

1. **Audit the class**: List every method and its primary responsibility
2. **Identify clusters**: Group methods by what domain they serve
3. **Define interfaces**: Create clear contracts for each new class
4. **Extract incrementally**: Move one cluster at a time, keeping tests passing
5. **Update dependencies**: Replace direct calls with new class instances
6. **Delete dead code**: Remove any methods that are no longer needed

### Code Examples (Good)

#### Fixed Example 1: Separated Python Classes

```python
class UserService:
    def __init__(self, db: Database, email: EmailService):
        self.db = db
        self.email = email

    def create_user(self, data): ...
    def delete_user(self, id): ...
    def send_welcome_email(self, user): ...


class PaymentService:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor

    def process_payment(self, order): ...
    def validate_credit_card(self, card): ...


class ReportService:
    def __init__(self, db: Database):
        self.db = db

    def generate_report(self, type): ...
    def export_to_csv(self, data): ...
    def import_from_csv(self, file): ...


class AuthService:
    def authenticate_user(self, creds): ...
    def refresh_token(self, token): ...
```

**Why this is better:** Each class has a single, clear responsibility. They're easier to test, understand, and modify independently.

#### Fixed Example 2: Composition Pattern

```javascript
class Application {
    constructor(
        userController,
        productController,
        orderController
    ) {
        this.users = userController;
        this.products = productController;
        this.orders = orderController;
    }
}

class UserController {
    createUser() { /* ... */ }
    updateUser() { /* ... */ }
}

class ProductController {
    addProduct() { /* ... */ }
    removeProduct() { /* ... */ }
}

class OrderController {
    placeOrder() { /* ... */ }
    cancelOrder() { /* ... */ }
}
```

**Why this is better:** Application coordinates between focused controllers, each handling a single domain.

### Prevention Strategies

- Set up linting rules to warn on file size (e.g., max 300 lines)
- Code review checklist includes "Does this class have a single responsibility?"
- Create new files/classes proactively when adding new features
- Regular refactoring sessions to split growing classes

---

## Exceptions

### When It's Acceptable

1. **Facade pattern**: A class that intentionally provides a simplified interface to a complex subsystem (but delegates, not implements)
2. **Generated code**: Auto-generated files from tools/frameworks that shouldn't be manually edited
3. **Test fixtures**: Large test setup classes that group related test data

### How to Document Exceptions

When this anti-pattern is intentional, document it with:

```python
# EXCEPTION: god-object
# Reason: This is a Facade that delegates to specialized services.
#         The class itself contains no business logic.
# Reviewed: 2026-01-20
class ApplicationFacade:
    """
    Facade providing simplified access to application subsystems.
    All methods delegate to specialized services.
    """
    pass
```

---

## Related Anti-Patterns

- [Spaghetti Code](./spaghetti-code.md) - Often found within God Objects
- [Deep Nesting](./deep-nesting.md) - Complex control flow in large methods

---

## References

- [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- [Refactoring: Improving the Design of Existing Code](https://refactoring.com/) - Martin Fowler
- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/) - Robert C. Martin
