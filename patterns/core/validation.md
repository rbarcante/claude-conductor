---
name: "Validation"
category: "Data Integrity"
tags:
  - validation
  - input
  - schema
  - sanitization
activation:
  keywords:
    - validate
    - validation
    - schema
    - input
    - sanitize
    - check
    - verify
    - constraint
  file_patterns:
    - "**/valid*.{js,ts,py,go,rs,java,kt}"
    - "**/schema*.{js,ts,py,go,rs,java,kt}"
    - "**/sanitize*.{js,ts,py,go,rs,java,kt}"
    - "**/*Validator.java"
    - "**/*Validation.java"
    - "**/*DTO.java"
version: "1.0"
last_updated: "2026-01-19"
---

# Validation

> Validate and sanitize input data at system boundaries with clear error messages and type safety.

---

## AI Quick Reference

### When to Apply
- Accepting user input (forms, API requests)
- Processing external data (files, webhooks, third-party APIs)
- Defining data models and schemas
- Creating API request/response contracts

### Core Principles
1. **Validate at Boundaries**: Check data when it enters your system
2. **Fail with Clarity**: Error messages should guide users to fix issues
3. **Whitelist over Blacklist**: Define what's allowed, not what's forbidden
4. **Sanitize after Validation**: Clean data only after confirming it's valid
5. **Type Coercion with Care**: Be explicit about type conversions

### Quick Implementation Checklist
- [ ] Define schemas for all external inputs
- [ ] Validate at API/controller layer
- [ ] Return structured error responses with field-level details
- [ ] Sanitize HTML/SQL only after validation passes
- [ ] Test with edge cases and malicious input
- [ ] Document validation rules in API specs

### Code Pattern (Pseudocode)
```
// Define validation schema
userSchema = {
    email: { type: string, format: email, required: true },
    age: { type: number, min: 0, max: 150 },
    username: { type: string, pattern: /^[a-z0-9_]{3,20}$/ }
}

// Validate and return structured result
function validateInput(data, schema) {
    errors = []

    for (field, rules in schema) {
        value = data[field]

        if (rules.required && isEmpty(value)) {
            errors.push({ field, message: `${field} is required` })
            continue
        }

        if (!matchesType(value, rules.type)) {
            errors.push({ field, message: `${field} must be a ${rules.type}` })
        }

        // Additional rule checks...
    }

    return { valid: errors.length === 0, errors, data: sanitize(data) }
}
```

### Key Decisions
| Decision Point | Recommended Choice | Rationale |
|----------------|-------------------|-----------|
| Schema library | Zod, Joi, JSON Schema | Type-safe, composable |
| Error format | Field-level array | Client can highlight fields |
| Sanitization | After validation | Don't sanitize invalid data |
| Validation location | API boundary | Single source of truth |

---

## Human Documentation

### Overview

Validation is the first line of defense against bad data, security attacks, and bugs. It ensures that only well-formed, expected data enters your system, making downstream code simpler and safer.

Good validation:
- Prevents security vulnerabilities (injection, XSS)
- Improves user experience with helpful error messages
- Simplifies internal code (no defensive checks everywhere)
- Documents expected data formats

### Detailed Explanation

#### Concept 1: Validation vs Sanitization

These are different concerns that should be handled separately:

| Aspect | Validation | Sanitization |
|--------|------------|--------------|
| **Purpose** | Check if data is acceptable | Clean data for safe use |
| **When** | Before processing | After validation passes |
| **On failure** | Reject with error | N/A (only sanitize valid data) |
| **Examples** | Email format, number range | HTML escaping, SQL escaping |

**Wrong**: Sanitize input, then validate
```javascript
// Bad: Sanitizing invalid data wastes effort and may hide issues
const cleaned = sanitizeHtml(input);
const valid = validateLength(cleaned);
```

**Right**: Validate first, then sanitize
```javascript
// Good: Only clean data that passes validation
const result = validate(input);
if (result.valid) {
    const cleaned = sanitizeHtml(result.data);
}
```

#### Concept 2: Error Message Design

Error messages should be:
- **Specific**: Tell users exactly what's wrong
- **Actionable**: Explain how to fix it
- **Localized**: Support multiple languages
- **Safe**: Don't expose internal details

```json
{
    "errors": [
        {
            "field": "email",
            "code": "INVALID_FORMAT",
            "message": "Please enter a valid email address",
            "details": {
                "expected": "user@example.com",
                "received": "not-an-email"
            }
        },
        {
            "field": "age",
            "code": "OUT_OF_RANGE",
            "message": "Age must be between 18 and 120",
            "details": {
                "min": 18,
                "max": 120,
                "received": 15
            }
        }
    ]
}
```

#### Concept 3: Layered Validation

Different layers have different validation responsibilities:

| Layer | Validates | Example |
|-------|-----------|---------|
| **Client** | UX feedback | Disable submit if form invalid |
| **API** | Structure, types, formats | Required fields, email format |
| **Service** | Business rules | User has permission, item in stock |
| **Database** | Constraints | Foreign keys, unique constraints |

Never rely solely on client-side validation—it can be bypassed.

### Implementation Examples

#### Example 1: Request Validation with Schema

```
// Define validation schema
createUserSchema = Schema({
    email: String(format = "email", errorMessage = "Invalid email format"),
    password: String(
        minLength = 8, errorMessage = "Password must be at least 8 characters",
        pattern = "[A-Z]", patternError = "Password must contain uppercase letter",
        pattern = "[0-9]", patternError = "Password must contain a number"
    ),
    age: Integer(
        min = 13, minError = "Must be at least 13 years old",
        max = 120, maxError = "Invalid age"
    ),
    username: String(
        minLength = 3, minError = "Username too short",
        maxLength = 20, maxError = "Username too long",
        pattern = "^[a-z0-9_]+$",
        patternError = "Username can only contain lowercase letters, numbers, and underscores"
    )
})

// Validation middleware
function validateRequest(schema):
    return function(request, response, next):
        result = schema.validate(request.body)

        if not result.success:
            return response.status(400).json({
                error: "Validation failed",
                details: result.errors.map(err => {
                    field: err.path,
                    message: err.message,
                    code: err.code
                })
            })

        request.validatedBody = result.data
        next()

// Usage
app.post("/users", validateRequest(createUserSchema), createUser)
```

#### Example 2: Custom and Cross-Field Validation

```
// Custom validation rule for phone numbers
phoneNumberRule = customValidator(
    function(value):
        return matchesPattern(value, "^\+?[1-9]\d{1,14}$"),
    errorMessage = "Invalid phone number format (E.164)"
)

// Custom rule for future dates
futureDateRule = customValidator(
    function(value):
        return value > currentDate(),
    errorMessage = "Date must be in the future"
)

// Cross-field validation (comparing two fields)
dateRangeSchema = Schema({
    startDate: Date(),
    endDate: Date()
}).crossFieldValidation(
    function(data):
        return data.endDate > data.startDate,
    errorMessage = "End date must be after start date",
    errorField = "endDate"
)

// Conditional validation (field required based on another field)
shippingSchema = Schema({
    deliveryType: Enum(["pickup", "delivery"]),
    address: String(optional = true)
}).conditionalValidation(
    function(data):
        return data.deliveryType != "delivery" or data.address is not null,
    errorMessage = "Address is required for delivery",
    errorField = "address"
)
```

### Best Practices

1. **Use Schema Libraries**: Don't write validation by hand. Libraries like Zod, Joi, or JSON Schema handle edge cases and provide consistent error formatting.

2. **Validate Types Strictly**: `"123"` is not the same as `123`. Be explicit about type coercion.

3. **Document with OpenAPI/JSON Schema**: Your validation schemas can generate API documentation automatically.

4. **Test Edge Cases**: Empty strings, null, undefined, very long strings, Unicode, negative numbers, boundary values.

5. **Rate Limit Validation Attempts**: Prevent attackers from probing your validation rules.

### Trade-offs and Considerations

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| Runtime validation (Zod) | Type inference, composable | Runtime overhead | TypeScript APIs |
| JSON Schema | Standard, language-agnostic | Verbose, no type inference | API documentation |
| Database constraints | Guaranteed integrity | Late failure, limited rules | Final safety net |
| GraphQL schemas | Built-in validation | GraphQL-specific | GraphQL APIs |

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Blacklist Validation

**What it looks like:**
```
function validateUsername(username):
    forbidden = ["admin", "root", "system"]

    if username.toLowerCase() in forbidden:
        return { valid: false, error: "Username not allowed" }

    return { valid: true }
```

**Why it's problematic:**
- Attackers can always find bypasses (unicode, encoding)
- List is never complete
- Doesn't validate format

**Better approach:**
```
// Whitelist: define what IS allowed
usernameSchema = String(
    minLength = 3,
    maxLength = 20,
    pattern = "^[a-z0-9_]+$"
).customValidator(
    function(name):
        return name not in reservedNames,
    errorMessage = "This username is reserved"
)
```

### Anti-Pattern 2: Silent Coercion

**What it looks like:**
```
function processAge(input):
    age = parseInteger(input) or 0  // Silently defaults to 0
    return saveUser({ age: age })
```

**Why it's problematic:**
- Hides data issues
- Saves incorrect data
- Hard to debug later

**Better approach:**
```
ageSchema = Integer(min = 0, max = 150)

function processAge(input):
    result = ageSchema.validate(input)

    if not result.success:
        throw ValidationError("age", "Must be a valid age")

    return saveUser({ age: result.data })
```

### Anti-Pattern 3: Client-Only Validation

**What it looks like:**
```
// Client-side form component
class SignupForm:
    email = ""

    function isValid():
        return matchesEmailPattern(email)

    function handleSubmit():
        if isValid():
            api.createUser({ email: email })  // Server trusts client

// Server endpoint
function handleCreateUser(request, response):
    // No validation! Trusts client blindly
    database.users.create(request.body)
```

**Why it's problematic:**
- Client validation easily bypassed (DevTools, cURL)
- Security vulnerabilities (injection)
- Inconsistent data in database

**Better approach:**
```
// Server ALWAYS validates
function handleCreateUser(request, response):
    result = userSchema.validate(request.body)

    if not result.success:
        return response.status(400).json({ errors: result.errors })

    database.users.create(result.data)
```

---

## Related Patterns

- [Error Handling](./error-handling.md) - How to handle validation errors
- [Configuration](./configuration.md) - Validate configuration at startup

---

## References

- [Zod Documentation](https://zod.dev/) - TypeScript-first schema validation
- [OWASP Input Validation](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) - Security perspective
- [JSON Schema](https://json-schema.org/) - Language-agnostic schema standard
