# Pattern Registry

This file serves as the central index for all patterns available in the Conductor Pattern Reference Layer.

## Overview

Patterns provide reusable solutions and best practices for common development challenges. They are organized into two categories:

1. **Core Patterns** - Language-agnostic patterns applicable across all technology stacks
2. **Stack Patterns** - Technology-specific patterns (future expansion)

## How to Use Patterns

Patterns are automatically surfaced during `/conductor:implement` when task descriptions match pattern activation keywords. You can also:

- Use `/conductor:patterns list` to see all available patterns
- Use `/conductor:patterns search <keyword>` to find relevant patterns
- Use `/conductor:patterns show <pattern-name>` to view a specific pattern

---

## Core Patterns

Language-agnostic patterns for fundamental development concerns.

| Pattern | Category | Description | Activation Keywords |
|---------|----------|-------------|---------------------|
| [Error Handling](./core/error-handling.md) | Resilience | Exception handling, error propagation, user-friendly messages | error, exception, catch, throw, try, handle |
| [Logging](./core/logging.md) | Observability | Log levels, structured logging, context inclusion | log, logging, logger, debug, info, warn, trace |
| [Configuration](./core/configuration.md) | Infrastructure | Config management, environment variables, secrets handling | config, configuration, environment, env, settings, secrets |
| [Validation](./core/validation.md) | Data Integrity | Input validation, schema validation, error messages | validate, validation, schema, input, sanitize, check |
| [Testing](./core/testing.md) | Quality | Test structure, mocking, assertions, coverage strategies | test, testing, unit, integration, mock, assert, coverage |

---

## Stack Patterns

Technology-specific patterns organized by stack. *Coming in future tracks.*

| Stack | Status | Description |
|-------|--------|-------------|
| TypeScript/JavaScript | Planned | Async/await patterns, type safety, module patterns |
| Python | Planned | Pythonic patterns, type hints, async patterns |
| Go | Planned | Go idioms, error handling, concurrency patterns |
| Rust | Planned | Ownership patterns, error handling, async patterns |

---

## Contributing Patterns

To add a new pattern:

1. Create a new markdown file in the appropriate directory (`core/` or `stack/<technology>/`)
2. Use the [TEMPLATE.md](./TEMPLATE.md) as your starting point
3. Ensure all required sections are complete
4. Add the pattern to this index with appropriate metadata
5. Test pattern surfacing with relevant task descriptions
